from flask import Flask, render_template, request, jsonify
from components.electrolyzer import Electrolyzer
from components.power_sources import SolarPowerSource, WindPowerSource
from components.storage import HydrogenStorage
from plots import plot_results

app = Flask(__name__)

# Store components and connections
components = {
    "electrolyzers": [],
    "power_sources": [],
    "storages": []
}
connections = []  # To keep track of connections between components


@app.route('/')
def index():
    """Render the simulation canvas."""
    return render_template('index.html')


@app.route('/add_component', methods=['POST'])
def add_component():
    """Add a component to the simulation based on user input."""
    data = request.json
    component_type = data['type']
    name = data['name']

    if component_type == 'electrolyzer':
        electrolyzer = Electrolyzer(name=name, capacity=10, efficiency=0.7)
        components['electrolyzers'].append(electrolyzer)
    elif component_type == 'solar_power':
        solar = SolarPowerSource(name=name, max_output=10)
        components['power_sources'].append(solar)
    elif component_type == 'wind_power':
        wind = WindPowerSource(name=name, max_output=8)
        components['power_sources'].append(wind)
    elif component_type == 'storage':
        storage = HydrogenStorage(name=name, max_capacity=100)
        components['storages'].append(storage)
    else:
        return jsonify({"status": "Error", "message": "Unknown component type"}), 400

    return jsonify({"status": f"{component_type} added", "name": name})

@app.route('/connect_components', methods=['POST'])
def connect_components():
    """Connect two components based on user interaction on the canvas."""
    data = request.json
    print(f"connect component: {data}")
    source_name = data['source']
    target_name = data['target']

    # Find source and target components from all possible types
    source = (
        next((c for c in components['power_sources'] if c.name == source_name), None) or
        next((c for c in components['electrolyzers'] if c.name == source_name), None) or
        next((c for c in components['storages'] if c.name == source_name), None)
    )
    target = (
        next((c for c in components['power_sources'] if c.name == target_name), None) or
        next((c for c in components['electrolyzers'] if c.name == target_name), None) or
        next((c for c in components['storages'] if c.name == target_name), None)
    )

    # Add connection if valid
    if source and target:
        target.connect(source)
        connections.append({"source": source_name, "target": target_name})
        return jsonify({"status": "Connected", "source": source_name, "target": target_name})

    return jsonify({"status": "Error", "message": "Invalid connection"}), 400


@app.route('/simulate', methods=['POST'])
def simulate():
    """Run the simulation and return the results."""
    # Reset simulation variables
    time_steps = 24
    power_inputs = []  # Clear previous values
    hydrogen_productions = []  # Clear previous values
    storage_levels = []  # Clear previous values

    print(connections)
    print(components)

    if components['electrolyzers'] and connections:
        print("Simulation starting...")

        for step in range(time_steps):
            for electrolyzer in components['electrolyzers']:
                electrolyzer.update(step)

                # Collect data consistently
                power_inputs.append(electrolyzer.current_power)
                hydrogen_productions.append(electrolyzer.hydrogen_production)

                if electrolyzer.storage:
                    storage_levels.append(electrolyzer.storage.get_storage_level())
                else:
                    storage_levels.append(0)

            # Debugging: Print lengths after each step
            print(f"Step {step}: Power Inputs: {len(power_inputs)}, "
                  f"Hydrogen Productions: {len(hydrogen_productions)}, "
                  f"Storage Levels: {len(storage_levels)}")

        # Ensure consistent array lengths before plotting
        min_length = min(len(power_inputs), len(hydrogen_productions), len(storage_levels))
        power_inputs = power_inputs[:min_length]
        hydrogen_productions = hydrogen_productions[:min_length]
        storage_levels = storage_levels[:min_length]

        plot_results(time_steps, power_inputs, hydrogen_productions, storage_levels)
        return jsonify({"status": "Simulation complete", "plots": "Plots generated"})

    return jsonify({"status": "Error", "message": "Components missing or not connected"}), 400


@app.route('/reset', methods=['POST'])
def reset_simulation():
    """Reset all components, connections, and simulation data."""
    components['electrolyzers'] = []
    components['power_sources'] = []
    components['storages'] = []
    connections.clear()
    return jsonify({"status": "Simulation reset successfully"})


if __name__ == '__main__':
    app.run(debug=True)

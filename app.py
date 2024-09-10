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


@app.route('/simulate', methods=['POST'])
def simulate():
    """Run the simulation and return the results."""
    time_steps = 24
    power_inputs, hydrogen_productions, storage_levels = [], [], []

    if components['electrolyzers']:
        for electrolyzer in components['electrolyzers']:
            for step in range(time_steps):
                electrolyzer.update(step)
                power_inputs.append(electrolyzer.current_power)
                hydrogen_productions.append(electrolyzer.hydrogen_production)
                if electrolyzer.storage:
                    storage_levels.append(electrolyzer.storage.get_storage_level())
                else:
                    storage_levels.append(0)

        plot_results(time_steps, power_inputs, hydrogen_productions, storage_levels)
        return jsonify({"status": "Simulation complete", "plots": "Plots generated"})

    return jsonify({"status": "Error", "message": "Components missing or not connected"}), 400


if __name__ == '__main__':
    app.run(debug=True)

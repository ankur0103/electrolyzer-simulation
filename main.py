import random

import matplotlib.pyplot as plt


class Electrolyzer:
    def __init__(self, capacity, efficiency):
        """
        Initialize the electrolyzer with a given capacity (Mega Watts) and efficiency (fraction).
        :param capacity: Maximum power input in MW
        :param efficiency: Efficiency of the electrolyzer (0 < efficiency <= 1)
        """
        self.capacity = capacity
        self.efficiency = efficiency
        self.power_source = None
        self.storage = None
        self.current_power = 0
        self.hydrogen_production = 0

    def produce_hydrogen(self, power_input):
        """
        Calculate hydrogen production based on power input and efficiency.
        :param power_input: Input power in MW
        :return: Produced hydrogen in MW
        """
        if power_input > self.capacity:
            power_input = self.capacity  # Limit input to capacity
        self.current_power = power_input
        self.hydrogen_production = self.current_power * self.efficiency
        return self.hydrogen_production

    def connect_power_source(self, power_source):
        """
        Connect a power source to the electrolyzer.
        :param power_source: An instance of a PowerSource class
        """
        self.power_source = power_source

    def connect_storage(self, storage):
        """
        Connect hydrogen storage to the electrolyzer.
        :param storage: An instance of a HydrogenStorage class
        """
        self.storage = storage

    def update(self, time_step):
        """
        Update the electrolyzer state based on input power from the power source.
        :param time_step: Current time step in the simulation
        """
        if self.power_source:
            power_input = self.power_source.get_power(time_step)
            hydrogen_produced = self.produce_hydrogen(power_input)
            if self.storage:
                self.storage.store_hydrogen(hydrogen_produced)


class PowerSource:
    def __init__(self, max_output):
        """
        Initialize the power source with a maximum output (MW).
        :param max_output: Maximum power output in MW
        """
        self.max_output = max_output

    def get_power(self, time_step):
        """
        Simulate variable power output, e.g., from renewable sources.
        :param time_step: Current time step in the simulation
        :return: Variable power output in MW
        """
        # Simulate variability using a random factor
        return random.uniform(0.5, 1.0) * self.max_output


class HydrogenStorage:
    def __init__(self, max_capacity):
        """
        Initialize hydrogen storage with a maximum capacity (MWh).
        :param max_capacity: Maximum storage capacity in MWh
        """
        self.max_capacity = max_capacity
        self.current_storage = 0

    def store_hydrogen(self, hydrogen_amount):
        """
        Store produced hydrogen, ensuring storage capacity is not exceeded.
        :param hydrogen_amount: Amount of hydrogen to store in MWh
        """
        potential_storage = self.current_storage + hydrogen_amount
        if potential_storage > self.max_capacity:
            self.current_storage = self.max_capacity  # Cap the storage at max capacity
        else:
            self.current_storage = potential_storage

    def get_storage_level(self):
        """
        Return the current storage level.
        :return: Current storage level in MWh
        """
        return self.current_storage


def run_simulation(electrolyzer, time_steps):
    """
    Run the simulation for a given number of time steps and collect results.
    :param electrolyzer: An instance of the Electrolyzer class
    :param time_steps: Number of time steps to run the simulation
    :return: Lists of power inputs, hydrogen productions, and storage levels
    """
    power_inputs = []
    hydrogen_productions = []
    storage_levels = []

    for step in range(time_steps):
        electrolyzer.update(step)
        power_inputs.append(electrolyzer.current_power)
        hydrogen_productions.append(electrolyzer.hydrogen_production)
        storage_levels.append(electrolyzer.storage.get_storage_level() if electrolyzer.storage else 0)

    return power_inputs, hydrogen_productions, storage_levels


def plot_results(time_steps, power_inputs, hydrogen_productions, storage_levels):
    """
    Plot the simulation results.
    :param time_steps: Number of time steps
    :param power_inputs: List of power input values over time
    :param hydrogen_productions: List of hydrogen production values over time
    :param storage_levels: List of storage level values over time
    """
    plt.figure(figsize=(20, 8))

    # Plot Power Input
    plt.subplot(3, 1, 1)
    plt.plot(range(time_steps), power_inputs, label='Power Input (MW)', color='b')
    plt.xlabel('Time (hours)')
    plt.ylabel('Power Input (MW)')
    plt.legend()

    # Plot Hydrogen Production
    plt.subplot(3, 1, 2)
    plt.plot(range(time_steps), hydrogen_productions, label='Hydrogen Production (MW)', color='g')
    plt.xlabel('Time (hours)')
    plt.ylabel('Hydrogen Production (MW)')
    plt.legend()

    # Plot Storage Level
    plt.subplot(3, 1, 3)
    plt.plot(range(time_steps), storage_levels, label='Storage Level (MWh)', color='r')
    plt.xlabel('Time (hours)')
    plt.ylabel('Storage Level (MWh)')
    plt.legend()

    plt.tight_layout()
    plt.show()


# Simulation parameters
capacity = 10  # MW
efficiency = 0.7
max_output = 10  # MW
max_storage_capacity = 100  # MWh
time_steps = 24  # 24 hours

# Initialize components
electrolyzer = Electrolyzer(capacity=capacity, efficiency=efficiency)
power_source = PowerSource(max_output=max_output)
storage = HydrogenStorage(max_capacity=max_storage_capacity)

# Connect components
electrolyzer.connect_power_source(power_source)
electrolyzer.connect_storage(storage)

# Run simulation
power_inputs, hydrogen_productions, storage_levels = run_simulation(electrolyzer, time_steps)

# Plot results
plot_results(time_steps, power_inputs, hydrogen_productions, storage_levels)

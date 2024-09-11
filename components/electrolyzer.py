# components/electrolyzer.py

from .base import Component
from .power_sources import PowerSource
from .storage import HydrogenStorage


class Electrolyzer(Component):
    """
    Electrolyzer class that simulates the production of hydrogen from input power.
    """

    def __init__(self, name, capacity, efficiency):
        """
        Initialize the electrolyzer with capacity and efficiency.
        :param name: Name of the electrolyzer
        :param capacity: Maximum capacity of the electrolyzer in MW
        :param efficiency: Efficiency of hydrogen production (fraction)
        """
        super().__init__(name)
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
        power_input = min(power_input, self.capacity)  # Limit input to capacity
        self.current_power = power_input
        self.hydrogen_production = self.current_power * self.efficiency
        return self.hydrogen_production

    def connect(self, component):
        """
        Connect another component (power source or storage) to the electrolyzer.
        :param component: Component to connect (PowerSource or HydrogenStorage)
        """
        if isinstance(component, PowerSource):
            self.power_source = component
        elif isinstance(component, HydrogenStorage):
            self.storage = component

    def update(self, time_step):
        """
        Update the electrolyzer state based on input power from the power source.
        :param time_step: Current time step in the simulation
        """
        if self.power_source:
            power_input = self.power_source.get_power(time_step)
            hydrogen_produced = self.produce_hydrogen(power_input)
            print(self.power_source, power_input, hydrogen_produced, "=====================")
            if self.storage:
                print(self.storage, "-----------")
                self.storage.store_hydrogen(hydrogen_produced)
                print("storage added")

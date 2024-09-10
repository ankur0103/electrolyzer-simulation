# components/power_sources.py

import random
from abc import ABC, abstractmethod

from .base import Component


class PowerSource(Component, ABC):
    """
    Abstract base class for different types of power sources.
    """

    def __init__(self, name, max_output):
        """
        Initialize a power source with a maximum output.
        :param name: Name of the power source
        :param max_output: Maximum power output in MW
        """
        super().__init__(name)
        self.max_output = max_output

    @abstractmethod
    def get_power(self, time_step):
        """
        Abstract method to get the power output at a given time step.
        Must be implemented by subclasses.
        :param time_step: Current time step in the simulation
        :return: Power output in MW
        """
        pass


class SolarPowerSource(PowerSource):
    """
    Simulates solar power output with a daily variation pattern.
    """

    def get_power(self, time_step):
        """
        Get power output based on the time of day, peaking at midday.
        :param time_step: Current time step in the simulation
        :return: Power output in MW with some randomness
        """
        peak = self.max_output
        time_of_day_factor = max(0, -0.05 * (time_step - 12) ** 2 + 1)  # Parabolic profile
        return peak * time_of_day_factor * random.uniform(0.8, 1.2)


class WindPowerSource(PowerSource):
    """
    Simulates wind power with random fluctuations.
    """

    def get_power(self, time_step):
        """
        Get power output with wind variability.
        :param time_step: Current time step in the simulation
        :return: Power output in MW
        """
        return random.uniform(0.3, 1.0) * self.max_output


class BatteryPowerSource(PowerSource):
    """
    Simulates power output from a battery storage system.
    """

    def __init__(self, name, max_output, battery_capacity):
        """
        Initialize the battery with maximum output and capacity.
        :param name: Name of the battery power source
        :param max_output: Maximum power output in MW
        :param battery_capacity: Total capacity of the battery in MWh
        """
        super().__init__(name, max_output)
        self.battery_capacity = battery_capacity
        self.current_charge = battery_capacity

    def get_power(self, time_step):
        """
        Get power output based on current charge, limited by max output.
        :param time_step: Current time step in the simulation
        :return: Power output in MW
        """
        discharge_rate = min(self.current_charge, self.max_output)
        self.current_charge -= discharge_rate
        return discharge_rate

    def recharge(self, amount):
        """
        Recharge the battery with a specified amount of energy.
        :param amount: Amount of energy to add to the battery in MWh
        """
        self.current_charge = min(self.battery_capacity, self.current_charge + amount)

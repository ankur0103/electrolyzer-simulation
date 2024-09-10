# components/storage.py

from .base import Component


class HydrogenStorage(Component):
    """
    Simulates hydrogen storage capabilities.
    """

    def __init__(self, name, max_capacity):
        """
        Initialize hydrogen storage with a maximum capacity.
        :param name: Name of the hydrogen storage
        :param max_capacity: Maximum storage capacity in MWh
        """
        super().__init__(name)
        self.max_capacity = max_capacity
        self.current_storage = 0

    def store_hydrogen(self, hydrogen_amount):
        """
        Store produced hydrogen, ensuring storage capacity is not exceeded.
        :param hydrogen_amount: Amount of hydrogen to store in MWh
        """
        potential_storage = self.current_storage + hydrogen_amount
        self.current_storage = min(potential_storage, self.max_capacity)

    def get_storage_level(self):
        """
        Return the current storage level.
        :return: Current storage level in MWh
        """
        return self.current_storage

# components/base.py

class Component:
    """
    Base class for all components in the simulation.
    """

    def __init__(self, name):
        """
        Initialize a component with a given name.
        :param name: Name of the component
        """
        self.name = name

    def update(self, time_step):
        """
        Update the state of the component for each time step.
        This method should be overridden by subclasses.
        :param time_step: Current time step in the simulation
        """
        pass

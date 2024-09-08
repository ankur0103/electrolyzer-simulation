# Electrolyzer Simulation Python Challenge

## Background
You are developing the backend for a no-code energy simulation platform. One of the key components in green hydrogen
production is the electrolyzer. Users can drag and drop an electrolyzer icon onto the simulation canvas, connect it to
other components, and run simulations to analyze its performance within the larger system.

## Task

Implement a Python class Electrolyzer that models the behavior of an electrolyzer in a green hydrogen production system.
The class should handle the following:

1. Initialize with configurable parameters (e.g., capacity, efficiency).
2. Calculate hydrogen production based on input power.
3. Manage energy balance (power in vs. hydrogen energy out).
4. Handle variable power input (e.g., from renewable sources).
5. Provide methods for connecting to other components (e.g., power sources, hydrogen storage).

## Requirements

1. Implement the Electrolyzer class with the following methods:
    - __init__(self, capacity, efficiency)
    - produce_hydrogen(self, power_input)
    - connect_power_source(self, power_source)
    - connect_storage(self, storage)
    - update(self, time_step)

2. Implement a simple PowerSource class to simulate variable power input.

3. Implement a basic HydrogenStorage class to store produced hydrogen.

4. Create a simulation loop that runs for 24 hours with 1-hour time steps, demonstrating the interaction between these
   components.

5. Plot the results showing power input, hydrogen production, and storage levels over time.

## Example Code Structure

import matplotlib.pyplot as plt

class Electrolyzer:
      def _init_(self, capacity, efficiency):
      # Initialize electrolyzer properties
      pass

    def produce_hydrogen(self, power_input):
        # Calculate hydrogen production based on power input
        pass

    def connect_power_source(self, power_source):
        # Connect a power source to the electrolyzer
        pass

    def connect_storage(self, storage):
        # Connect hydrogen storage to the electrolyzer
        pass

    def update(self, time_step):
        # Update electrolyzer state for each time step
        pass

 class PowerSource:
     # Implement a simple power source with variable output
     pass
 
 class HydrogenStorage:
      # Implement basic hydrogen storage functionality
     pass

## Simulation setup and loop

    electrolyzer = Electrolyzer(capacity=10, efficiency=0.7)
    power_source = PowerSource()
    storage = HydrogenStorage()
    
    electrolyzer.connect_power_source(power_source)
    electrolyzer.connect_storage(storage)
    
    time_steps = 24  # 24 hours
    results = []
    
    for step in range(time_steps):
       Run simulation steps and collect results
        pass

## Plot results

Use matplotlib to create graphs of power input, hydrogen production, and storage levels

(You can be creative and use something else)

## Evaluation Criteria

1. Correctness of the electrolyzer model and calculations
2. Proper use of object-oriented programming principles
3. Handling of time-based simulation and component interactions
4. Code clarity, comments, and overall structure
5. Appropriate use of Python libraries (e.g., for plotting)
6. Consideration of edge cases and error handling

Please implement this simulation and be prepared to discuss your approach, any assumptions made, and how you would
extend this model to handle more complex scenarios in the energy planning platform.
# app.py

from components.electrolyzer import Electrolyzer
from components.power_sources import SolarPowerSource, WindPowerSource, BatteryPowerSource
from components.storage import HydrogenStorage
from plots import plot_results

# Simulation setup
electrolyzer = Electrolyzer(name="Electrolyzer1", capacity=10, efficiency=0.7)
solar_power = SolarPowerSource(name="Solar Plant", max_output=10)
wind_power = WindPowerSource(name="Wind Turbine", max_output=8)
battery_power = BatteryPowerSource(name="Battery Storage", max_output=5, battery_capacity=50)

# Connect the solar power source to the electrolyzer
electrolyzer.connect(solar_power)

# Connect hydrogen storage to the electrolyzer
storage = HydrogenStorage(name="Hydrogen Tank", max_capacity=100)
electrolyzer.connect(storage)

# Simulation parameters
time_steps = 24  # 24 hours
power_inputs = []
hydrogen_productions = []
storage_levels = []

# Simulation loop
for step in range(time_steps):
    electrolyzer.update(step)
    power_inputs.append(electrolyzer.current_power)
    hydrogen_productions.append(electrolyzer.hydrogen_production)
    storage_levels.append(storage.get_storage_level())

# Plotting results
plot_results(time_steps, power_inputs, hydrogen_productions, storage_levels)

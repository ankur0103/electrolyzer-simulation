# plots.py

import matplotlib.pyplot as plt


def plot_results(time_steps, power_inputs, hydrogen_productions, storage_levels):
    """
    Plot simulation results including power inputs, hydrogen production, and storage levels.
    :param time_steps: Total number of time steps in the simulation
    :param power_inputs: List of power inputs over time
    :param hydrogen_productions: List of hydrogen production over time
    :param storage_levels: List of storage levels over time
    """
    plt.figure(figsize=(14, 6))

    plt.subplot(3, 1, 1)
    plt.plot(range(time_steps), power_inputs, label='Power Input (MW)')
    plt.ylabel('Power Input (MW)')
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.plot(range(time_steps), hydrogen_productions, label='Hydrogen Production (MW)', color='g')
    plt.ylabel('Hydrogen Production (MW)')
    plt.legend()

    plt.subplot(3, 1, 3)
    plt.plot(range(time_steps), storage_levels, label='Storage Level (MWh)', color='r')
    plt.xlabel('Time (hours)')
    plt.ylabel('Storage Level (MWh)')
    plt.legend()

    plt.tight_layout()
    plt.show()

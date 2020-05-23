from simulate.simulate import Simulation
import matplotlib.pyplot as plt
import numpy as np


def task_1():
    simulation = Simulation(1, [2], [0])
    simulation.simulate()
    neurons = simulation.network.populations[-1].neurons
    delta_t = list()
    delta_w = list()
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(40, 10))
    time = np.arange(0, simulation.total_time)
    i = 0
    colors = ["green", "orange"]
    for neuron in neurons:
        delta_t.append(neuron.delta_t)
        delta_w.append(neuron.delta_w)
        ax1.scatter(neuron.delta_t, neuron.delta_w, color=colors[i])
        ax2.plot(time, neuron.voltage, color=colors[i])
        ax3.plot(time, neuron.current, color=colors[i])
        i += 1
        print(neuron.last_spike_time)
        # print(neuron.voltage)
        # print(neuron.current)
    print(delta_t)
    print(delta_w)
    # ax1.scatter(delta_t, delta_w)
    plt.show()

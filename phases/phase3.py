from simulate.simulate import Simulation
import matplotlib.pyplot as plt
import numpy as np
from network.network import Network
from simulate.constant import TOTAL_TIME, DT
import random


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
    ax1.set_ylabel("delta_w")
    ax1.set_xlabel("time difference")
    ax2.set_ylabel("voltage")
    ax2.set_xlabel("time")
    ax3.set_ylabel("current")
    ax3.set_xlabel("time")
    print(delta_t)
    print(delta_w)
    # ax1.scatter(delta_t, delta_w)
    plt.show()


def task_2():
    network = Network(1, [12], [0])
    population = network.populations[0]
    population.add_layer(10)
    population.add_layer(2)
    population.connect_layer_fully()
    for neuron in population.neurons:
        neuron.set_current(0, TOTAL_TIME, 0)
    # encode(population, [1, 0, 1, 1, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 1, 1, 0])
    encode(population, [1, 0, 1, 1, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 1, 1, 1, 0])
    weights = dict()
    pre_synaptic_neurons = population.neurons[:10]
    post_synaptic_neurons = population.neurons[10:]
    for pre_synaptic_neuron in pre_synaptic_neurons:
        for post_synaptic_neuron in post_synaptic_neurons:
            if pre_synaptic_neuron not in weights.keys():
                weights[pre_synaptic_neuron] = dict()
            weights[pre_synaptic_neuron][post_synaptic_neuron] = list()
    for t in range(TOTAL_TIME):
        network.update_voltage(t)
        for pre_synaptic_neuron in pre_synaptic_neurons:
            for post_synaptic_neuron in post_synaptic_neurons:
                weights[pre_synaptic_neuron][post_synaptic_neuron].append(
                    population.synapse.adjacency[pre_synaptic_neuron][post_synaptic_neuron]['weight'])
    for neuron in population.neurons:
        if neuron in population.synapse.adjacency.keys():
            for post_synaptic_neuron in population.synapse.adjacency[neuron].keys():
                print(population.synapse.adjacency[neuron][post_synaptic_neuron]['weight'], end=" ")
            print()
    # fig, ax = plt.subplots(1, 1, figsize=(50, 30))
    # time = np.arange(0, TOTAL_TIME)
    # ax.plot(time, population.neurons[0].voltage)
    # ax.plot(time, population.neurons[10].voltage)
    # plt.show()
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(50, 100))
    time = np.arange(0, TOTAL_TIME)
    for pre_synaptic_neuron in pre_synaptic_neurons:
        for post_synaptic_neuron in post_synaptic_neurons:
            ax1.plot(time, weights[pre_synaptic_neuron][post_synaptic_neuron])
    # ax2.plot(time, population.neurons[0].voltage)
    ax2.plot(time, population.neurons[11].voltage)
    ax2.plot(time, population.neurons[10].voltage)
    plt.show()


def encode(population, pattern, pattern2=None):
    neurons = population.neurons
    interval_time = int(TOTAL_TIME / 14)
    interval_times = [[(i - 1) * interval_time, i * interval_time] for i in range(1, 14)]
    first_interval = interval_times[: len(interval_times) // 2]
    second_interval = interval_times[len(interval_times) // 2 + 2:]
    print(first_interval)
    for i in range(len(first_interval)):
        if i % 2 == 0:
            for index, neuron in enumerate(neurons):
                if index < 10 and pattern[index] == 1:
                    neuron.set_current(first_interval[i][0], first_interval[i][1], 1)
        # else:
        #     index = random.randint(0, 9)
        #     neurons[index].set_current(first_interval[i][0], first_interval[i][1], 1)
    if pattern2 is not None:
        for i in range(len(second_interval)):
            if i % 2 == 0:
                for index, neuron in enumerate(neurons):
                    if index < 10 and pattern2[index] == 1:
                        neuron.set_current(second_interval[i][0], second_interval[i][1], 1.15)
        # else:
        #     index = random.randint(0, 9)
        #     neurons[index].set_current(second_interval[i][0], second_interval[i][1], 1)


def task_3():
    network = Network(1, [12], [1])
    population = network.populations[0]
    population.add_layer(10)
    population.add_layer(3)
    population.connect_layer_fully()
    neuron_10 = population.neurons[10]
    neuron_11 = population.neurons[11]
    neuron_12 = population.neurons[12]
    population.synapse.connect(neuron_12, neuron_10)
    population.synapse.connect(neuron_12, neuron_11)
    for neuron in population.neurons:
        neuron.set_current(0, TOTAL_TIME, 0)
    encode(population, [1, 0, 1, 1, 1, 0, 0, 0, 0, 0])
    for t in range(TOTAL_TIME):
        network.update_voltage(t)
    for neuron in population.neurons:
        if neuron in population.synapse.adjacency.keys():
            for post_synaptic_neuron in population.synapse.adjacency[neuron].keys():
                print(population.synapse.adjacency[neuron][post_synaptic_neuron], end=" ")
            print()

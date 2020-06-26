from network.network import Network
from simulate.constant import TOTAL_TIME, DT
import matplotlib.pyplot as plt
import numpy as np
import random


def task_1():
    network = Network(1, [12], [0])
    population = network.populations[0]
    population.add_layer(10)
    population.add_layer(2)
    population.connect_layer_fully()
    population.synapse.target_neurons = [population.neurons[10]]
    population.learn_method = "rstdp"
    for neuron in population.neurons:
        neuron.set_current(0, TOTAL_TIME, 0)
    encode(population, [1, 0, 1, 1, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 1, 1, 0])
    pre_synaptic_neurons, post_synaptic_neurons, weights = initialize_weight(population)

    for t in range(TOTAL_TIME):
        network.update_voltage(t)
        update_weight(pre_synaptic_neurons, post_synaptic_neurons, weights, population)
        if t == TOTAL_TIME // 2:
            population.synapse.target_neurons = [population.neurons[11]]
    show_weight_plot(population, pre_synaptic_neurons, post_synaptic_neurons, weights)


def update_weight(pre_synaptic_neurons, post_synaptic_neurons, weights, population):
    for pre_synaptic_neuron in pre_synaptic_neurons:
        for post_synaptic_neuron in post_synaptic_neurons:
            weights[pre_synaptic_neuron][post_synaptic_neuron].append(
                population.synapse.adjacency[pre_synaptic_neuron][post_synaptic_neuron]['weight'])


def initialize_weight(population):
    weights = dict()
    pre_synaptic_neurons = population.neurons[:10]
    post_synaptic_neurons = population.neurons[10:]
    for pre_synaptic_neuron in pre_synaptic_neurons:
        for post_synaptic_neuron in post_synaptic_neurons:
            if pre_synaptic_neuron not in weights.keys():
                weights[pre_synaptic_neuron] = dict()
            weights[pre_synaptic_neuron][post_synaptic_neuron] = list()
    return pre_synaptic_neurons, post_synaptic_neurons, weights


def show_weight_plot(population, pre_synaptic_neurons, post_synaptic_neurons, weights):
    for neuron in population.neurons:
        if neuron in population.synapse.adjacency.keys():
            for post_synaptic_neuron in population.synapse.adjacency[neuron].keys():
                print(population.synapse.adjacency[neuron][post_synaptic_neuron]["weight"], end=" ")
            print()
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(50, 100))
    time = np.arange(0, TOTAL_TIME)
    i = 0
    for pre_synaptic_neuron in pre_synaptic_neurons:
        for post_synaptic_neuron in post_synaptic_neurons:
            line, = ax1.plot(time, weights[pre_synaptic_neuron][post_synaptic_neuron])
            line.set_label(i)
            ax1.legend()
            i += 1
    # ax.plot(time, weights[population.neurons[6]][population.neurons[11]])
    # # ax.plot(time, weights[population.neurons[7]][population.neurons[11]])
    ax2.plot(time, population.neurons[10].voltage, color="red")
    ax2.plot(time, population.neurons[11].voltage, color="green")
    plt.show()


def encode(population, pattern, pattern2=None):
    neurons = population.neurons
    interval_time = int(TOTAL_TIME / 14)
    interval_times = [[(i - 1) * interval_time, i * interval_time] for i in range(1, 14)]
    first_interval = interval_times[: len(interval_times) // 2]
    second_interval = interval_times[len(interval_times) // 2 + 2:]
    print(second_interval)
    for i in range(len(first_interval)):
        if i % 2 == 0:
            for index, neuron in enumerate(neurons):
                if index < 10 and pattern[index] == 1:
                    neuron.set_current(first_interval[i][0], first_interval[i][1], 1)

    if pattern2 is not None:
        for i in range(len(second_interval)):
            if i % 2 == 0:
                for index, neuron in enumerate(neurons):
                    if index < 10 and pattern2[index] == 1:
                        neuron.set_current(second_interval[i][0], second_interval[i][1], 1)


def task_2():
    network = Network(1, [10], [3])
    population = network.populations[0]
    population.connect_randomly(0.3)
    cluster_number = 3
    output_populations = [population.neurons[i * 2: (i + 1) * 2] for i in range(0, cluster_number)]
    print(output_populations)
    input_population = population.neurons[6: 10]
    for neuron in population.neurons:
        neuron.set_current(0, TOTAL_TIME, 0)
    population.synapse.target_neurons = output_populations[0]
    population.learn_method = "rstdp"
    encode_task2(input_population)
    size_activity_neuron = [[] for i in range(0, cluster_number)]
    time = np.arange(0, TOTAL_TIME)
    for t in range(TOTAL_TIME):
        network.update_voltage(t)
        for index, output_neurons in enumerate(output_populations):
            activity = 0
            for neuron in output_neurons:
                activity += neuron.voltage[t]
            size_activity_neuron[index].append(activity / len(output_neurons))
    fig, ax = plt.subplots(1, 1, figsize=(50, 100))
    for i in range(cluster_number):
        ax.scatter(time, size_activity_neuron[i])
    plt.show()


def encode_task2(input_neurons):
    pattern = list()
    for i in range(3):
        pattern.append(1)
    for i in range(2):
        pattern.append(0)
    neurons = input_neurons
    interval_time = int(TOTAL_TIME / 14)
    interval_times = [[(i - 1) * interval_time, i * interval_time] for i in range(1, 14)]
    input_interval_time = interval_times[3: 11]
    for i in range(len(input_interval_time)):
        # if i % 2 == 0:
        for index, neuron in enumerate(neurons):
            if pattern[index] == 1:
                neuron.set_current(input_interval_time[i][0], input_interval_time[i][1], 1)

# encode(population, )

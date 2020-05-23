import numpy as np
from simulate.constant import DT, TOTAL_TIME


class Synapse:
    def __init__(self):
        self.total_time = TOTAL_TIME
        self.adjacency = dict()
        self.reverse_adjacency = dict()
        self.dt = DT
        self.post = list()
        self.delay = 0
        self.maximum_weight = 1
        self.landa = 0.1
        self.weight = np.zeros(self.total_time)
        self.tau_positive = 2
        self.tau_negative = 4
        self.amplitude_positive = 0.4
        self.amplitude_negative = -0.4
        self.delta_w = 0
        self.delta_t = 0

    def connect(self, pre_synaptic_neuron, post_synaptic_neuron):
        if pre_synaptic_neuron not in self.adjacency.keys():
            self.adjacency[pre_synaptic_neuron] = list()
        self.adjacency[pre_synaptic_neuron].append([post_synaptic_neuron, 0])
        if post_synaptic_neuron not in self.reverse_adjacency.keys():
            self.reverse_adjacency[post_synaptic_neuron] = list()
        self.reverse_adjacency[post_synaptic_neuron].append([pre_synaptic_neuron, 0])

    def update_weight(self, current_time):
        c_corr_11 = self.landa * (self.maximum_weight - self.weight)
        # dw_per_dt = c_corr_11 * self.pre.voltage[current_time] * self.post[-1].voltage[current_time]
        # self.weight = dw_per_dt * self.dt

    def stdp(self, neuron):
        if neuron in self.adjacency.keys():
            maximum_post_synaptic_time = 0
            for post_synaptic in self.adjacency[neuron]:
                maximum_post_synaptic_time = post_synaptic[0].last_spike_time
            delta_t = maximum_post_synaptic_time - neuron.last_spike_time
            self.add_delta_t_delta_w(neuron, delta_t)
        elif neuron in self.reverse_adjacency:
            maximum_pre_synaptic_time = 0
            for pre_synaptic_neuron in self.reverse_adjacency[neuron]:
                maximum_pre_synaptic_time = pre_synaptic_neuron[0].last_spike_time
            delta_t = neuron.last_spike_time - maximum_pre_synaptic_time
            self.add_delta_t_delta_w(neuron, delta_t)

    def add_delta_t_delta_w(self, neuron, delta_t):
        if delta_t > 0:
            delta_w = self.amplitude_positive * np.exp(-1 * abs(delta_t) / self.tau_positive)
        else:
            delta_w = self.amplitude_negative * np.exp(-1 * abs(delta_t) / self.tau_negative)
        neuron.delta_t.append(delta_t)
        neuron.delta_w.append(delta_w)
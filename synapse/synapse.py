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
            self.adjacency[pre_synaptic_neuron] = dict()
        self.adjacency[pre_synaptic_neuron][post_synaptic_neuron] = 0.4

    def stdp(self, neuron):
        if neuron in self.adjacency.keys():
            maximum_post_synaptic_time = 0
            for post_synaptic_neuron in self.adjacency[neuron].keys():
                if maximum_post_synaptic_time <= post_synaptic_neuron.last_spike_time:
                    maximum_post_synaptic_time = post_synaptic_neuron.last_spike_time
            delta_t = maximum_post_synaptic_time - neuron.last_spike_time
            delta_w = self._add_delta_t_delta_w(neuron, delta_t)
            for post_synaptic_neuron in self.adjacency[neuron].keys():
                self.adjacency[neuron][post_synaptic_neuron] += delta_w
        else:
            maximum_pre_synaptic_time = 0
            pre_synaptic_neurons = list()
            for pre_synaptic_neuron in self.adjacency.keys():
                if neuron in self.adjacency[pre_synaptic_neuron].keys():
                    if maximum_pre_synaptic_time <= pre_synaptic_neuron.last_spike_time:
                        maximum_pre_synaptic_time = pre_synaptic_neuron.last_spike_time
                    pre_synaptic_neurons.append(pre_synaptic_neuron)
            delta_t = neuron.last_spike_time - maximum_pre_synaptic_time
            delta_w = self._add_delta_t_delta_w(neuron, delta_t)
            for pre_synaptic_neuron in pre_synaptic_neurons:
                self.adjacency[pre_synaptic_neuron][neuron] += delta_w

    def _add_delta_t_delta_w(self, neuron, delta_t):
        if delta_t > 0:
            delta_w = self.amplitude_positive * np.exp(-1 * abs(delta_t) / self.tau_positive)
        else:
            delta_w = self.amplitude_negative * np.exp(-1 * abs(delta_t) / self.tau_negative)
        neuron.delta_t.append(delta_t)
        neuron.delta_w.append(delta_w)
        return delta_w

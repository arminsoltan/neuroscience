import numpy as np
from simulate.simulate import Simulation


class Synapse(Simulation):
    def __init__(self, neuron):
        super().__init__()
        self.pre = neuron
        self.post = list()
        self.delay = 0
        self.learn = Learn

    def connect(self, post_synaptic_neurons):
        for neuron in post_synaptic_neurons:
            self.post.append(neuron)


class Learn(Synapse, Simulation):
    tau_positive = 0.4
    tau_negative = 0.4
    amplitude_positive = 0.4
    amplitude_negative = 0.4
    delta_w = 0

    def stdp(self):
        minimum_post_synaptic_spike_time = self.total_time + 100
        for neuron in self.post:
            minimum_post_synaptic_spike_time = min(neuron.last_spike_time, minimum_post_synaptic_spike_time)
        delta_t = self.pre.last_spike_time - minimum_post_synaptic_spike_time
        self.delta_w = self.amplitude_positive * np.exp(-1 * abs(delta_t) / self.tau_positive)

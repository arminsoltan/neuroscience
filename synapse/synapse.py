import numpy as np
from simulate.constant import DT, TOTAL_TIME
import random


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
        self.amplitude_positive = 4
        self.amplitude_negative = -0.8
        self.delta_w = 0
        self.delta_t = 0
        self.tau_c = 2
        self.tau_d = 1
        self.target_neurons = None

    def connect(self, pre_synaptic_neuron, post_synaptic_neuron):
        # print(self.adjacency)
        if pre_synaptic_neuron not in self.adjacency.keys():
            self.adjacency[pre_synaptic_neuron] = dict()
        self.adjacency[pre_synaptic_neuron][post_synaptic_neuron] = dict()
        self.adjacency[pre_synaptic_neuron][post_synaptic_neuron]['weight'] = random.uniform(0.1, 0.4)
        self.adjacency[pre_synaptic_neuron][post_synaptic_neuron]['dopamine'] = 0.1
        self.adjacency[pre_synaptic_neuron][post_synaptic_neuron]['synaptic_tag'] = 0.2
        self.adjacency[pre_synaptic_neuron][post_synaptic_neuron]['dopamine_activity'] = 0

    def stdp(self, neuron):
        if neuron in self.adjacency.keys():
            for post_synaptic_neuron in self.adjacency[neuron].keys():
                delta_t = post_synaptic_neuron.last_spike_time - neuron.last_spike_time
                delta_w = self._add_delta_t_delta_w(neuron, delta_t)
                self.adjacency[neuron][post_synaptic_neuron]['weight'] += delta_w
                # print(delta_t, delta_w, "##########")
        else:
            for pre_synaptic_neuron in self.adjacency.keys():
                if neuron in self.adjacency[pre_synaptic_neuron].keys():
                    delta_t = neuron.last_spike_time - pre_synaptic_neuron.last_spike_time
                    delta_w = self._add_delta_t_delta_w(neuron, delta_t)
                    if delta_t == neuron.last_spike_time:
                        delta_w = -1 * abs(delta_w)
                        self.adjacency[pre_synaptic_neuron][neuron]['weight'] /= 2
                    self.adjacency[pre_synaptic_neuron][neuron]['weight'] += delta_w

    def _add_delta_t_delta_w(self, neuron, delta_t):
        if delta_t > 0:
            delta_w = self.amplitude_positive * np.exp(-1 * abs(delta_t) / self.tau_positive)
        else:
            delta_w = self.amplitude_negative * np.exp(-1 * abs(delta_t) / self.tau_negative)
        neuron.delta_t.append(delta_t)
        neuron.delta_w.append(delta_w)
        return delta_w

    def rstdp(self, neuron, spike_neurons):
        self._give_reward(neuron, spike_neurons)
        # print("hell")
        if neuron in self.adjacency.keys():
            for post_synaptic_neuron in self.adjacency[neuron].keys():
                delta_t = post_synaptic_neuron.last_spike_time - neuron.last_spike_time
                d, s, c = self._get_rstdp_params(neuron, post_synaptic_neuron)
                if neuron in spike_neurons:
                    dc_per_dt = -1 * c / self.tau_c + self._add_delta_t_delta_w(neuron, delta_t)
                else:
                    dc_per_dt = -1 * c / self.tau_c
                c += dc_per_dt * self.dt
                dd_per_dt = -1 * d / self.tau_d
                d += dd_per_dt * self.dt
                s += c * d
                s = max(s, 0)
                self._update_rstdp_params(d, s, c, neuron, post_synaptic_neuron)
        else:
            for pre_synaptic_neuron in self.adjacency.keys():
                if neuron in self.adjacency[pre_synaptic_neuron].keys():
                    d, s, c = self._get_rstdp_params(pre_synaptic_neuron, neuron)
                    delta_t = neuron.last_spike_time - pre_synaptic_neuron.last_spike_time
                    if neuron in spike_neurons:
                        dc_per_dt = -1 * c / self.tau_c + self._add_delta_t_delta_w(neuron, delta_t)
                    else:
                        dc_per_dt = -1 * c / self.tau_c
                    c += dc_per_dt * self.dt
                    dd_per_dt = -1 * d / self.tau_d + self.adjacency[pre_synaptic_neuron][neuron]['dopamine_activity']
                    d += dd_per_dt * self.dt
                    s += c * d
                    # print(s, d, c)
                    s = max(s, 0)
                    self._update_rstdp_params(d, s, c, pre_synaptic_neuron, neuron)

    def _give_reward(self, neuron, spike_neurons):
        if neuron not in spike_neurons:
            return
        reward = -0.99
        if neuron in self.target_neurons:
            reward *= -1
        for pre_synaptic_neuron in self.adjacency.keys():
            if neuron in self.adjacency[pre_synaptic_neuron].keys():
                if abs(
                        neuron.last_spike_time - pre_synaptic_neuron.last_spike_time) < 15 and neuron.last_spike_time != 0:
                    self.adjacency[pre_synaptic_neuron][neuron]['dopamine_activity'] = reward
                else:
                    self.adjacency[pre_synaptic_neuron][neuron]['dopamine_activity'] = 0

    def _get_rstdp_params(self, pre_synaptic_neuron, post_synaptic_neuron):
        d = self.adjacency[pre_synaptic_neuron][post_synaptic_neuron]['dopamine']
        s = self.adjacency[pre_synaptic_neuron][post_synaptic_neuron]['weight']
        c = self.adjacency[pre_synaptic_neuron][post_synaptic_neuron]['synaptic_tag']
        return d, s, c

    def _update_rstdp_params(self, d, s, c, pre_synaptic_neuron, post_synaptic_neuron):
        self.adjacency[pre_synaptic_neuron][post_synaptic_neuron]['dopamine'] = d
        self.adjacency[pre_synaptic_neuron][post_synaptic_neuron]['weight'] = s
        self.adjacency[pre_synaptic_neuron][post_synaptic_neuron]['synaptic_tag'] = c
        self.adjacency[pre_synaptic_neuron][post_synaptic_neuron]['dopamine_activity'] = max(
            self.adjacency[pre_synaptic_neuron][post_synaptic_neuron]['dopamine_activity'] - 0.01, 0)

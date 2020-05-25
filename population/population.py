from neuron.neuron import Neuron
from synapse.synapse import Synapse
from simulate.constant import TOTAL_TIME


class Population:
    def __init__(self, exc_count, inh_count):
        self.exc_count = exc_count
        self.inh_count = inh_count
        self.neurons = list()
        self._create_neurons()
        self.synapse = Synapse()
        self.spike_neurons = list()
        self.layers = list()

    def _create_neurons(self):
        for i in range(self.exc_count):
            neuron = Neuron('lif')
            neuron.set_current_randomly(0, TOTAL_TIME)
            self.neurons.append(neuron)

    def fully_connected_one_way(self):
        for i in range(0, len(self.neurons)):
            for j in range(i + 1, len(self.neurons)):
                self.synapse.connect(self.neurons[i], self.neurons[j])

    def update_voltage(self, current_time):
        self.spike_neurons = list()
        for neuron in self.neurons:
            neuron.update_voltage(current_time)
            if neuron.is_spike:
                self.spike_neurons.append(neuron)

    def update_weight(self, current_time):
        for neuron in self.spike_neurons:
            if neuron in self.synapse.adjacency.keys():
                for post_synaptic_neuron in self.synapse.adjacency[neuron]:
                    post_synaptic_neuron[0].last_pre_synaptic_spike_time = current_time
        for neuron in self.spike_neurons:
            self.synapse.stdp(neuron)

    def add_layer(self, layer_size):
        count = 0
        for layer in self.layers:
            count += len(layer)
        layer = list()
        for i in range(layer_size):
            layer.append(self.neurons[i + count])
        self.layers.append(layer)

    def connect_layer_fully(self):
        for i in range(1, len(self.layers)):
            pre_layer = self.layers[i - 1]
            post_layer = self.layers[i]
            for pre_synaptic_neuron in pre_layer:
                for post_synaptic_neuron in post_layer:
                    self.synapse.connect(pre_synaptic_neuron, post_synaptic_neuron)


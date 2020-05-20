import numpy as np
from random import randint
from scipy import interpolate
from sklearn.preprocessing import MinMaxScaler
from synapse.synapse import Synapse
from simulate.simulate import Simulation


class Neuron(Simulation):
    def __init__(self):
        super().__init__()
        self.voltage_rest = 0
        self.voltage_reset = 0
        self.voltage = np.zeros(self.total_time)
        self.firing_threshold = 0
        self.current = np.zeros(self.total_time)
        self.synapse = Synapse(self)
        self.last_adjacent_spike_time = 0
        self.last_spike_time = 0
        self.spike_times = list()

    def set_current(self, t1, t2, value):
        self.current[t1:t2] = value

    def set_current_randomly(self, t1, t2):
        x = np.linspace(0, 1, t2 - t1)
        y = randint(0, 100) * np.sin(randint(0, 100) * x) + randint(0, 100) * np.cos(randint(0, 100) * x)
        y = MinMaxScaler(feature_range=(-1, 1)).fit_transform(y.reshape(-1, 1)).reshape(-1)
        y = [abs(x) for x in y]
        self.current[t1:t2] = y

    def connect(self, neurons):
        self.synapse.connect(neurons)


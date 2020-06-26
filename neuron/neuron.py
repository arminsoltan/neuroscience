import numpy as np
from random import randint
from scipy import interpolate
from sklearn.preprocessing import MinMaxScaler
from synapse.synapse import Synapse

from .constant import params, SIMULATION_MODEL
from simulate.constant import DT, TOTAL_TIME


class Neuron:
    def __init__(self, simulation_model, model="exc"):
        self.model = model
        self.total_time = TOTAL_TIME
        self.voltage_rest = params['voltage_rest']
        self.voltage_reset = params['voltage_reset']
        self.voltage = np.zeros(self.total_time)
        self.firing_threshold = params['firing_threshold']
        self.current = np.zeros(self.total_time)
        self.last_pre_synaptic_spike_time = 0
        self.last_spike_time = 0
        self.spike_times = list()
        self.simulation_model = SIMULATION_MODEL[simulation_model](self)
        self.delta_t = list()
        self.delta_w = list()
        self.is_spike = False

    def set_current(self, t1, t2, value):
        self.current[t1:t2] = value

    def set_current_randomly(self, t1, t2):
        x = np.linspace(0, 1, t2 - t1)
        y = randint(0, 100) * np.sin(randint(0, 100) * x) + randint(0, 100) * np.cos(randint(0, 100) * x)
        y = MinMaxScaler(feature_range=(-1, 1)).fit_transform(y.reshape(-1, 1)).reshape(-1)
        y = [5 * abs(x) for x in y]
        self.current[t1:t2] = y

    def update_voltage(self, current_time):
        self.simulation_model.compute_voltage(t=current_time)

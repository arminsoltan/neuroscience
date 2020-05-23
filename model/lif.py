class LIF:
    def __init__(self, neuron):
        self.dt = 0.1
        self.neuron = neuron
        self.tau = 6
        self.resistance = 2

    def compute_voltage(self, t):
        dv_per_dt = (-(self.neuron.voltage[t - 1] - self.neuron.voltage_rest) + self.resistance * self.neuron.current[t]) / self.tau
        self.neuron.is_spike = False
        self.neuron.voltage[t] = dv_per_dt * self.dt + self.neuron.voltage[t - 1]
        if self.neuron.voltage[t] >= self.neuron.firing_threshold:
            self.neuron.voltage[t - 1] = self.neuron.firing_threshold
            self.neuron.voltage[t] = self.neuron.voltage_reset
            self.neuron.last_spike_time = t
            self.neuron.is_spike = True

from simulate.simulate import Simulation


class LIF(Simulation):
    def __init__(self, neuron):
        super().__init__()
        self.neuron = neuron
        self.tau = 0
        self.resistance = 0

    def compute_voltage(self, t):
        dv_per_dt = -(self.neuron.voltage[t - 1] - self.neuron.voltage_rest) + self.resistance * self.neuron.current[t]
        self.neuron.voltage[t] = self.tau * dv_per_dt * self.dt
        if self.neuron.voltage[t] >= self.neuron.firing_threshold:
            self.neuron.voltage[t-1] = self.neuron.firing_threshold
            self.neuron.voltage[t] = self.neuron.voltage_reset

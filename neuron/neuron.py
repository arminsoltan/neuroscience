class Neuron:
    def __init__(self):
        self.model = 'inhibitory'
        self.voltage_rest = 0
        self.voltage_reset  = 0
        self.firing_threshold = 0
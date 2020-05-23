from simulate.constant import params as simulation_params
from model.lif import LIF

params = {
    'voltage_rest': -0.6,
    'voltage_reset': -0.7,
    'firing_threshold': 0.1,
    'total_time': simulation_params['total_time']
}

SIMULATION_MODEL = {
    'lif': LIF
}
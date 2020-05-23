from .constant import params
from network.network import Network
from simulate.constant import DT, TOTAL_TIME


class Simulation:
    def __init__(self, population_count, exc_neurons_count, inh_neurons_count):
        self.dt = DT
        self.current_time = 0
        self.total_time = TOTAL_TIME
        self.population_count = population_count
        self.exc_neurons_count = exc_neurons_count
        self.inh_neurons_count = inh_neurons_count
        self.network = Network(self.population_count, self.exc_neurons_count, self.inh_neurons_count)

    def simulate(self):
        for population in self.network.populations:
            population.fully_connected_one_way()

        for t in range(1, self.total_time):
            self.network.update_voltage(t)


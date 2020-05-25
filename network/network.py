from population.population import Population


class Network:
    def __init__(self, population_count, exc_neurons_count, inh_neurons_count):
        self.populations = list()
        self.population_count = population_count
        self.exc_neurons_count = exc_neurons_count
        self.inh_neurons_count = inh_neurons_count
        self._create_population()

    def _create_population(self):
        for i in range(self.population_count):
            population = Population(self.exc_neurons_count[i], self.inh_neurons_count[i])
            self.populations.append(population)

    def update_voltage(self, current_time):
        for population in self.populations:
            population.update_voltage(current_time)
            population.update_weight(current_time)

    def connect(self, population1, population2):
        for neuron1 in population1:
            for neuron2 in population2:

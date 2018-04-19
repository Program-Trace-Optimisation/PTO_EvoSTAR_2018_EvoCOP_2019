import random
import math

######################### EVOLUTIONARY ALGORITHM #########################

class EA:
    """ Evolutionary Algorithm Class """

    def __init__(self, ops, budget):
        self.ops = ops

        self.NUMBER_GENERATION = int(math.sqrt(budget))
        self.POPULATION_SIZE = int(budget / self.NUMBER_GENERATION)
        self.TRUNCATION_RATE = 0.5
        #print("EA: GENO_SIZE = " + str(GENO_SIZE))
        #print("EA: POPULATION_SIZE = " + str(self.POPULATION_SIZE))

        self.data = []

    def run(self):

        population = self.create_pop()
        fitness_population = self.evaluate_pop(population)
        self.data = [max(fitness_population)] * self.POPULATION_SIZE

        for _ in range(self.NUMBER_GENERATION):
            mating_pool = self.select_pop(population, fitness_population)
            offspring_population = self.crossover_pop(mating_pool)
            population = self.mutate_pop(offspring_population)
            fitness_population = self.evaluate_pop(population)
            self.data += [max(fitness_population)] * self.POPULATION_SIZE

        return self.best_pop(population, fitness_population)

    #####

    def create_pop(self):
        return [ self.ops.create_ind() for _ in range(self.POPULATION_SIZE) ]

    def evaluate_pop(self, population):
        return [ self.ops.evaluate_ind(individual) for individual in population ]

    def select_pop(self, population, fitness_population):
        sorted_population = sorted(zip(population, fitness_population), key = lambda ind_fit: ind_fit[1], reverse=True)
        return [ individual for individual, fitness in sorted_population[:int(math.ceil(self.POPULATION_SIZE * self.TRUNCATION_RATE))]]

    def crossover_pop(self, population):
        return [ self.ops.crossover_ind(random.choice(population), random.choice(population)) for _ in range(self.POPULATION_SIZE) ]

    def mutate_pop(self, population):
        return [ self.ops.mutate_ind(individual) for individual in population ]

    def best_pop(self, population, fitness_population):
        return sorted(zip(population, fitness_population), key = lambda ind_fit: ind_fit[1], reverse=True)[0]

##########################################################################

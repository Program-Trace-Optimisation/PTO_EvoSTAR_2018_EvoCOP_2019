import random, copy
import math

######################### PARTICLE SWARM OPTIMISATION #########################

class PS:
    """ Particle Swarm Class """

    def __init__(self, ops, budget):
        self.ops = ops

	self.NUMBER_GENERATION = int(math.sqrt(budget))
        self.POPULATION_SIZE = int(budget / self.NUMBER_GENERATION)

        self.data = []

    def run(self):

        population = self.create_pop()
        personal_best_population = copy.copy(population)
        global_best, global_best_fitness = self.get_best_pop(personal_best_population)
        self.data = [global_best_fitness] * self.POPULATION_SIZE

        for _ in range(self.NUMBER_GENERATION):
            population = self.convex_combination_pop(population, personal_best_population, [global_best]*self.POPULATION_SIZE)
            population = self.mutation_pop(population)
            personal_best_population = self.selection_pop(personal_best_population, population)
            global_best, global_best_fitness = self.get_best_pop(personal_best_population)
            self.data += [global_best_fitness] * self.POPULATION_SIZE

        return (global_best, global_best_fitness)

    #####

    def create_pop(self):
        return [ self.ops.create_ind() for _ in range(self.POPULATION_SIZE) ]

    def get_best_pop(self, population):
        best_ind = max(population, key=self.ops.evaluate_ind)
        return best_ind, self.ops.evaluate_ind(best_ind)

    def convex_combination_pop(self, pop1, pop2, pop3):
        return [ self.ops.convex_combination_ind([ind1, ind2, ind3]) for (ind1, ind2, ind3) in zip(pop1, pop2, pop3) ]

    def mutation_pop(self, population):
        return [ self.ops.mutate_ind(individual) for individual in population ]

    def selection_pop(self, pop1, pop2):
        return [ max(ind1, ind2, key=self.ops.evaluate_ind) for (ind1, ind2) in zip(pop1, pop2) ]

##########################################################################

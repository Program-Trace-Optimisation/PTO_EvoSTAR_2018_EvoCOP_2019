import random
import math

#################### Microbial Genetic Algorithm ####################

''' Define the Microbial Genetic Algoithm following source code outlined in 
    http://users.sussex.ac.uk/~inmanh/MicrobialGA_ECAL2009.pdf  '''


class MGA:
    """ Microbial Genetic Algorithm Class"""

    def __init__(self, ops, budget):
        self.ops = ops

        self.NUMBER_GENERATION = int(math.sqrt(budget))
        self.POPULATION_SIZE = int(budget / self.NUMBER_GENERATION)
        self.INFECTION_RATE = 0.5
        self.MUTATION_RATE = 0.5
        self.DEME_SIZE = 5

        self.data = []

    def run(self):
        population = self.create_pop()
        fitness_population = self.evaluate_pop(population)
        self.data = [max(fitness_population)] * self.POPULATION_SIZE

        for _ in range(self.NUMBER_GENERATION):
            A = int(self.POPULATION_SIZE * random.random())
            B = int((A + 1 + self.DEME_SIZE * random.random()) % self.POPULATION_SIZE)
            winner_pos, winner, loser_pos, loser = self.evaluate_genotypes(population, A, B)
            population[winner_pos] = winner #Put winner back in population untouched
            loser = self.infect_loser(winner,loser,self.INFECTION_RATE, self.MUTATION_RATE) #infect and mutate loser
            population[loser_pos] = loser
            fitness_population = self.evaluate_pop(population)

        return self.best_pop(population, fitness_population)

    #####

    def create_pop(self):
        return [ self.ops.create_ind() for _ in range(self.POPULATION_SIZE) ]

    def evaluate_pop(self, population):
        return [ self.ops.evaluate_ind(individual) for individual in population ]

    def infect_loser(self, winner, loser, infection_rate, mutation_rate):
        return self.ops.microbial_infect_and_mutate_ind(winner,loser,infection_rate, mutation_rate)

    def evaluate_genotypes(self, population, candidate_a, candidate_b):
        candidate_a_fitness = self.ops.evaluate_ind(population[candidate_a])
        candidate_b_fitness = self.ops.evaluate_ind(population[candidate_b])

        if candidate_a_fitness > candidate_b_fitness :
            return candidate_a, population[candidate_a], candidate_b, population[candidate_b]
        else:
            return candidate_b, population[candidate_b], candidate_a, population[candidate_a]

    def best_pop(self, population, fitness_population):
        return sorted(zip(population, fitness_population), key = lambda ind_fit: ind_fit[1], reverse=True)[0]
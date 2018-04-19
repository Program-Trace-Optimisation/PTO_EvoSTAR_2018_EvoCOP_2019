import random

######################### RANDOM SEARCH #########################

class RS:
    """ Random Search Class """

    def __init__(self, ops, budget):
        self.ops = ops
        
        self.NUMBER_GENERATION = budget
        self.data = []

    def run(self):
        individual = self.ops.create_ind()
        fitness_individual = self.ops.evaluate_ind(individual)
        self.data = [fitness_individual]
        
        for _ in range(self.NUMBER_GENERATION):
            offspring = self.ops.create_ind()
            fitness_offspring = self.ops.evaluate_ind(offspring)
            if fitness_offspring >= fitness_individual:
                individual = offspring
                fitness_individual = fitness_offspring
            self.data.append(fitness_individual)
            
        return (individual, fitness_individual)

#################################################################
    

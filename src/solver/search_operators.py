from collections import namedtuple
import random, copy

from POLY_REP import POLY_REP

Sol = namedtuple('Sol', ['pheno', 'geno'])

class OPS:
    """ Search Operators for the Trace Representation """

    def __init__(self, fitness, fine_ops, tracer):
        self.fitness = fitness
        self.tracer = tracer
        self.rep = POLY_REP(fine_ops) # polymorphic representation

    ##### COARSE OPERATORS (REPRESENTATION INDEPENDENT) #####

    def create_ind(self):
        return Sol._make(self.tracer.get_trace())
 
    def evaluate_ind(self, sol):
        return self.fitness(sol.pheno)

    def fix_ind(self, sol_geno):
        return Sol._make(self.tracer.play_trace(sol_geno))


    ##### COARSE OPERATORS #####
        
    def mutate_ind(self, sol):
        mut_prob = 1.0/len(sol.geno)
        offspring_geno = { addr : (self.rep.perturb(elem) if random.random() < mut_prob else elem) for addr, elem in sol.geno.items() }
        return self.fix_ind(offspring_geno) # fix geno and get pheno

    def crossover_ind(self, sol1, sol2):
        offspring_geno = sol1.geno.copy()
        offspring_geno.update({ addr : (self.rep.blend(elem, sol1.geno[addr]) if addr in sol1.geno else elem) for addr, elem in sol2.geno.items() })
        return self.fix_ind(offspring_geno) # fix geno and get pheno

    def convex_combination_ind(self, mating_pool):
        geno_pool = [sol.geno for sol in mating_pool] # extract genotypes
        offspring_keys = []
        for geno in geno_pool: # get all keys
            offspring_keys += geno.keys()
        offspring_geno = {}
        for addr in set(offspring_keys): # remove repeated keys
            parents = [ geno[addr] for geno in geno_pool if addr in geno ]
            offspring_geno[addr] = self.rep.combine(parents) # are we sure there is always a parent?
        return self.fix_ind(offspring_geno) # fix geno and get pheno



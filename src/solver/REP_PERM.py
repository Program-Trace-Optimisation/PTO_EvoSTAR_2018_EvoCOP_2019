import random
from REP import REP

class PERM(REP):
    """ Search Operators for Permutations """

    def __init__(self, *args):
        self.population, self.k = args

    def perturb(self, entry):
        
        return random.choice([self.swap_mutation, self.reversal_mutation])(entry)
    
    def swap_mutation(self, entry):
    
        typ, output = entry

        swap = random.sample(range(len(output)), 2)
        perturbed_output = output[:]
        perturbed_output[swap[0]], perturbed_output[swap[1]] = perturbed_output[swap[1]], perturbed_output[swap[0]] # swap

        return (typ, perturbed_output)

    def reversal_mutation(self, entry):
    
        typ, output = entry

        reversal = sorted(random.sample(range(len(output)+1), 2))
        perturbed_output = output[:reversal[0]] + output[reversal[0]:reversal[1]][::-1] + output[reversal[1]:] # reversal

        return (typ, perturbed_output)
       
    
    #FIXME: add PMX    

    #FIXME: add mutiparent sorting crossover

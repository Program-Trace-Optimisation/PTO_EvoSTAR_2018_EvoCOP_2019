import random
from REP import REP

class PERM(REP):
    """ Search Operators for Permutations """

    def __init__(self, *args):
        self.population, self.k = args

    # FIXME do we need to copy output, ie perturbed_output = output[:],
    # to avoid altering output itself?
    def perturb(self, entry):
        
        typ, output = entry

        swap = random.sample(range(len(output)), 2)
        perturbed_output = output
        perturbed_output[swap[0]], perturbed_output[swap[1]] = perturbed_output[swap[1]], perturbed_output[swap[0]] # swap

        return (typ, perturbed_output)

    
    #FIXME: add PMX    

    #FIXME: add mutiparent sorting crossover


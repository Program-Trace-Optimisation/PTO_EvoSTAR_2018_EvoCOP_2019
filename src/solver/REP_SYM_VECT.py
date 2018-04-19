import random
from REP import REP

class SYM_VECT(REP):
    """ Search Operators for Symbols """

    def __init__(self, *args):
        self.population, self.k = args
         
    #inherit this from superclass
    #def reset(self, (f, args, output)):
    #    return (f, args, f(*args)) # resample (reset)
    

    def perturb(self, entry):

        typ, output = entry

        perturbed_output = [ random.choice(self.population) if random.random() < 1.0/self.k else elem for elem in output ]

        return (typ, perturbed_output)


    def blend(self, entry1, entry2): # blends a single entry of the trace

        (typ, output1), (_, output2) = entry1, entry2
       
        combined_output = [ random.choice([elem1, elem2]) for elem1, elem2 in zip(output1, output2) ]

        return (typ, combined_output)
            

    def combine(self, entry_pool):

        typ = entry_pool[0][0]
        outputs = [output for (_, output) in entry_pool]

        combined_output = [ random.choice(elems) for elems in zip(outputs) ]

        return (typ, combined_output)
  

#####


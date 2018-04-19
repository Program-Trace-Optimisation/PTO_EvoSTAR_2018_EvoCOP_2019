import random
from REP import REP

class SYM(REP):
    """ Search Operators for Symbol """

    def __init__(self, *args):
        self.population = args[0]
         
    #inherit this from superclass
    #def reset(self, (f, args, output)):
    #    return (f, args, f(*args)) # resample (reset)
    

    def perturb(self, entry):

        typ, output = entry

        if len(self.population) == 1: # if len of input sequence is 1
            perturbed_output = output
        else:
            perturbed_output = output
            while perturbed_output == output:
                perturbed_output = random.choice(self.population) # resample until get a different choice (generalised bit-flip)

        return (typ, perturbed_output)


    #inherit this from superclass
    #def blend(self, entry1, entry2): # blends a single entry of the trace
    #
    #    (f1, args1, output1), (f2, args2, output2) = entry1, entry2
    #   
    #    combined_output = [ random.choice([elem1, elem2]) for elem1, elem2 in zip(output1, output2) ]
    #
    #    return (f1, args1, combined_output)
            

    #def combine(self, entry_pool):
    #
    #    outputs = [output for (_, _, output) in entry_pool]
    #
    #    combined_output = [ random.choice(elems) for elems in zip(outputs) ]
    #
    #    return (f1, args1, combined_output)
  

#####


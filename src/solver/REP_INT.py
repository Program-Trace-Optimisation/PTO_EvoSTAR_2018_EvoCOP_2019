import random
import math
from REP import REP

class INT(REP):
    """ Search Operators for Integers """

    def __init__(self, *args):
        self.start, self.stop, self.step = args
         
    #inherit this from superclass
    #def reset(self, (f, args, output)):
    #    return (f, args, f(*args)) # resample (reset)
    

    def perturb(self, entry):
        
        typ, output = entry

        step_size = int(math.ceil(random.expovariate(1))) * self.step # multi-step mutation with one expected step
        perturbed_output = output + (step_size if random.random() < 0.5 else -step_size)
        if perturbed_output < self.start or perturbed_output >= self.stop:
            perturbed_output = output

        return (typ, perturbed_output)


    def blend(self, entry1, entry2): # blends a single entry of the trace

        (typ, output1), (_, output2) = entry1, entry2

        if output1 == output2:
            combined_output = output1
        else:
            combined_output = random.randrange(min(output1, output2), max(output1, output2), self.step)

        return (typ, combined_output)    
            
    def combine(self, entry_pool):

        (typ, _) = entry_pool[0]
        outputs = [output for ( _, output) in entry_pool]

        min_outputs, max_outputs = min(outputs), max(outputs)
        if min_outputs == max_outputs:
            combined_output = min_outputs
        else:
            combined_output = random.randrange(min_outputs, max_outputs, self.step)

        return (typ, combined_output)


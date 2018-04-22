#from __future__ import print_function
import random, copy

    ##### GENERIC REPRESENTATION #####

class REP:
    """ Search Operators for Generic Trace Entry """

    def reset(self, entry):
        (f, args), _ = entry
        return ((f, args), f(*args)) # resample (reset)


    def perturb(self, entry): # perturbs a single entry of the trace
        (f, args), _ = entry
        return ((f, args), f(*args)) # reset mutation


    def blend(self, entry1, entry2): # blends a single entry of the trace
        #(f1, args1, output1), (f2, args2, output2) = entry1, entry2
        return random.choice([entry1,entry2])


    def combine(self, entry_pool):
        return random.choice(entry_pool)


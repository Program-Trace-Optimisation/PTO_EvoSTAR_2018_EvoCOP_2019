import random
from REP import REP

class REAL(REP):
    """ Search Operators for Real Numbers """

    def __init__(self, *args):
        self.a, self.b = args

         
    #inherit this from superclass
    #def reset(self, (f, args, output)):
    #    return (f, args, f(*args)) # resample (reset)

    
    def perturb(self, entry):

        (f,args) = entry[0]
        
        #mutation step
        samples = [f(*args) for _ in range(2)] # FIXME: remove dependency to f and args
        a, b = self.a, self.b
        if self.a == -float('inf'):
            a = min(samples)
        if self.b == float('inf'):
            b = max(samples)
        mut_step = (b-a)/10.0
        
        return random.choice([self.creep_mutation, self.gauss_mutation])(entry, mut_step)
    
    def gauss_mutation(self, entry, mut_step):

        typ, output = entry    

        perturbed_output = output + random.gauss(0,mut_step)
        perturbed_output = min(self.b, max(self.a, perturbed_output)) # ensure mutated value is within range

        return (typ, perturbed_output)

    def creep_mutation(self, entry, mut_step):
    
        typ, output = entry    
        
        perturbed_output = output + (random.random() - 0.5)*mut_step
        perturbed_output = min(self.b, max(self.a, perturbed_output)) # ensure mutated value is within range

        return (typ, perturbed_output)


    def blend(self, entry1, entry2):
        return random.choice([self.line_crossover, self.discrete_crossover])(entry1, entry2)

    def line_crossover(self, entry1, entry2):
        
        (typ, output1), (_, output2) = entry1, entry2
        combined_output = random.uniform(output1, output2)
        return (typ, combined_output)
        # can be written in 1 line: return (entry1[0], random.uniform(entry1[1], entry2[1]))
        

    def discrete_crossover(self, entry1, entry2): 
        
        (typ, output1), (_, output2) = entry1, entry2
        combined_output = random.choice([output1, output2]) 
        return (typ, combined_output)            

    '''
    def extended_line_crossover(self, entry1, entry2): # blends a single entry of the trace
        
        (f1, args1, output1), (f2, args2, output2) = entry1, entry2

        #FIXME: add extended line crossover

        #crossover_function = random.choice([line, discrete])
        #combined_output = crossover_function(output1, output2)
        return (f1, args1, combined_output)
    '''


    def combine(self, entry_pool):
        return random.choice([self.line_combine, self.discrete_combine, self.extended_line_combine])(entry_pool)        

    def line_combine(self, entry_pool):

        typ = entry_pool[0][0]
        outputs = [output for (_, output) in entry_pool]
        combined_output = random.uniform(min(outputs), max(outputs)) 
        return (typ, combined_output)

    def discrete_combine(self, entry_pool):

        typ = entry_pool[0][0]
        outputs = [output for (_, output) in entry_pool]
        combined_output = random.choice(outputs) 
        return (typ, combined_output)

    def extended_line_combine(self, entry_pool):

        typ = entry_pool[0][0]
        outputs = [output for (_, output) in entry_pool]
        min_output, max_output = min(outputs), max(outputs)
        ext_min_output = min_output - (max_output-min_output)*0.2
        ext_max_output = max_output + (max_output-min_output)*0.2
        combined_output = random.uniform(ext_min_output, ext_max_output) 
        return (typ, combined_output) # FIXME: must check that the output is in range

'''
    def extended_line_combine(self, entry_pool):

        (f1, args1, output1) = entry_pool[0]
        outputs = [output for (_, _, output) in entry_pool]
        combined_output = return random.choice(outputs) 
        return (f1, args1, combined_output)

        #def discrete(outputs):
        #    return random.choice(outputs) # discrete crossover

        #FIXME: add extended line recombination

        #recombination_function = random.choice([line, discrete])
        #combined_output = recombination_function(outputs)
        return (f1, args1, combined_output)
'''
    

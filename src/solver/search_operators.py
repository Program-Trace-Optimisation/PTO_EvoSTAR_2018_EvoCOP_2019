from __future__ import print_function
import random, copy
#import tracer


class OPS:
    """ Search Operators for the Trace Representation """

    def __init__(self, randsol, fitness, fine_ops, tracer):
        self.randsol = randsol
        self.fitness = fitness
        self.fine_ops = fine_ops
        self.tracer = tracer

    def create_ind(self):
        return self.tracer.get_trace(self.randsol)
 
    def evaluate_ind(self, x):
        return self.fitness(x[0])

    def fix_ind(self, x):
        return self.tracer.play_trace(self.randsol, x)

    AVG_SIZE = {} # memoise avg size in a class variable to prevent recomputation in different solve calls
    def avg_size_ind(self):
        
        if not self.randsol in OPS.AVG_SIZE:

            #print("computing avg size", end="")
            curr_cum_size, curr_iter = sum([len(self.create_ind()[1]) for _ in range(1000)]), 1000
            curr_avg_size = 1.0 * curr_cum_size / curr_iter
            prev_avg_size = 0
            while abs(1-prev_avg_size/curr_avg_size) > 0.001: # coverged within 1% tolerance?
                #print(".", end="")
                prev_avg_size = curr_avg_size
                curr_cum_size += sum([len(self.create_ind()[1]) for _ in range(1000)])
                curr_iter += 1000
                curr_avg_size = 1.0 * curr_cum_size / curr_iter
            
            OPS.AVG_SIZE[self.randsol] = int(curr_avg_size)
            #print(" average trace size: ", int(curr_avg_size))
            
        return OPS.AVG_SIZE[self.randsol]

    ##### COARSE OPERATORS #####
        
    def mutate_ind(self, (pheno, geno)):
        mut_prob = 1.0/len(geno)
        offspring_geno = { addr : ((REP.factory(elem, self.fine_ops)).perturb(elem) if random.random() < mut_prob else elem) for addr, elem in geno.items() }
        return self.fix_ind(offspring_geno) # fix geno and get pheno

    def crossover_ind(self, (pheno1, geno1), (pheno2, geno2)):
        offspring_geno = geno1.copy()
        offspring_geno.update({ addr : ((REP.factory(elem, self.fine_ops)).blend(elem, geno1[addr]) if addr in geno1 else elem) for addr, elem in geno2.items() })
        return self.fix_ind(offspring_geno) # fix geno and get pheno

    def convex_combination_ind(self, mating_pool):
        geno_pool = zip(*mating_pool)[1] # extract genotypes
        offspring_keys = []
        for geno in geno_pool: # get all keys
            offspring_keys += geno.keys()
        offspring_geno = {}
        for addr in set(offspring_keys): # remove repeated keys
            parents = [ geno[addr] for geno in geno_pool if addr in geno ]
            offspring_geno[addr] = (REP.factory(parents[0], self.fine_ops)).combine(parents) # are we sure there is always a parent?
        return self.fix_ind(offspring_geno) # fix geno and get pheno


    ##### REPRESENTATIONS FOR FINE OPERATORS #####

class REP:
    """ Search Operators for the Trace Entry Representations """

    @staticmethod
    def factory((f, args, output), fine_ops):

        if not fine_ops:
            return REP() # use generic coarse entry operations defined in REP
            
        if f.__name__ == "random" or f.__name__ == "uniform": 
            return Real(*args) # Real number representation

        if f.__name__ == "choice":
            return Cardinal() # Integer/Binary (cardinal) representation

        if f.__name__ == "randint": 
            return Ordinal() # Integer (ordinal) representation
        
        if f.__name__ == "shuffle":
            return Permutation() # Permutation representation
 
        #else:
        return REP() # fine ops not available, use coarse ops


    def reset(self, (f, args, output)):
        return (f, args, f(*args)) # resample (reset)


    def perturb(self, (f, args, output)): # perturbs a single entry of the trace
        return (f, args, f(*args)) # reset mutation


    def blend(self, (f1, args1, output1), (f2, args2, output2)): # blends a single entry of the trace
        return random.choice([(f1, args1, output1),(f2, args2, output2)])


    def combine(self, entry_pool):
        return random.choice(entry_pool)

#####
      
class Real(REP):
    """ Search Operators for Real Numbers """

    def __init__(self, *args):
        self.a, self.b = (0, 1) if not args else (min(args), max(args))
         
    #inherit this from superclass
    #def reset(self, (f, args, output)):
    #    return (f, args, f(*args)) # resample (reset)
    

    def perturb(self, (f, args, output)):

        def creep(output):
            return output + (random.random() - 0.5)*(self.b-self.a)/10.0

        def gauss(output):
            return output + random.gauss(0, (self.b-self.a)/10.0)

        mutation_function = random.choice([creep, gauss]) # pick at random when more than one mutation operator is available
        perturbed_output = min(self.b, max(self.a, mutation_function(output))) # ensure mutated value is within range
        return (f, args, perturbed_output)


    def blend(self, (f1, args1, output1), (f2, args2, output2)): # blends a single entry of the trace

        if (f1, args1) != (f2, args2):                                          # if incompatible parents, 
            return REP.blend(self, (f1, args1, output1), (f2, args2, output2))  # use coarse operator

        def line(p1,p2):
            return random.uniform(p1, p2) # line crossover

        def discrete(p1, p2):
            return random.choice([output1, output2]) # discrete crossover

        #FIXME: add extended line crossover

        crossover_function = random.choice([line, discrete])
        combined_output = crossover_function(output1, output2)
        return (f1, args1, combined_output)
            

    def combine(self, entry_pool):

        (f1, args1, _) = entry_pool[0]
        if [(f, args) for (f, args, output) in entry_pool].count((f1, args1)) < len(entry_pool): # if incompatible,
            return REP.combine(self, entry_pool)                                                 # use coarse operator    
        outputs = [output for (_, _, output) in entry_pool]

        def line(outputs):
            return random.uniform(min(outputs), max(outputs)) # line crossover

        def discrete(outputs):
            return random.choice(outputs) # discrete crossover

        #FIXME: add extended line recombination

        recombination_function = random.choice([line, discrete])
        combined_output = recombination_function(outputs)
        return (f1, args1, combined_output)

#####

class Cardinal(REP):
    """ Search Operators for Symbols """

    #inherit this from superclass
    #def __init__(self, *args):
    #    pass
         
    #inherit this from superclass
    #def reset(self, (f, args, output)):
    #    return (f, args, f(*args)) # resample (reset)
    

    def perturb(self, (f, args, output)):
        if len(*args) == 1: # if len of input sequence is 1
            perturbed_output = output
        else:
            perturbed_output = output
            while perturbed_output == output:
                perturbed_output = f(*args) # resample until get a different choice (generalised bit-flip)
        return (f, args, perturbed_output)

    #inherit this from superclass
    #def blend(self, (f1, args1, output1), (f2, args2, output2)): # blends a single entry of the trace
    #    pass
            

    #inherit this from superclass
    #def combine(self, entry_pool):
    #    pass   

#####

class Ordinal(REP):
    """ Search Operators for Integers """

    def __init__(self, *args):
        self.a, self.b = args
         
    #inherit this from superclass
    #def reset(self, (f, args, output)):
    #    return (f, args, f(*args)) # resample (reset)
    

    def perturb(self, (f, args, output)):

        def creep(output):
            return output + (1 if random.random() < 0.5 else -1)

        def gauss(output):
            return output + int(random.gauss(0, (b-a)/10.0))

        mutation_function = random.choice([creep, gauss]) # pick at random when more than one mutation operator is available
        perturbed_output = min(self.b, max(self.a, mutation_function(output))) # ensure mutated value is within range
        return (f, args, perturbed_output)


    def blend(self, (f1, args1, output1), (f2, args2, output2)): # blends a single entry of the trace

        if (f1, args1) != (f2, args2):                                          # if incompatible parents, 
            return REP.blend(self, (f1, args1, output1), (f2, args2, output2))  # use coarse operator

        combined_output = random.randomint(output1, output2)
        return (f1, args1, combined_output)
    
            
    def combine(self, entry_pool):

        (f1, args1, _) = entry_pool[0]
        if [(f, args) for (f, args, output) in entry_pool].count((f1, args1)) < len(entry_pool): # if incompatible,
            return REP.combine(self, entry_pool)                                                 # use coarse operator    
        outputs = [output for (_, _, output) in entry_pool]

        combined_output = random.randomint(min(outputs), max(outputs))
        return (f1, args1, combined_output)

#####

class Permutation(REP):
    """ Search Operators for Permutations """

    # FIXME do we need to copy output, ie perturbed_output = output[:],
    # to avoid altering output itself?
    def perturb(self, (f, args, output)):
        swap = random.sample(range(len(output)), 2)
        perturbed_output = output
        perturbed_output[swap[0]], perturbed_output[swap[1]] = perturbed_output[swap[1]], perturbed_output[swap[0]] # swap
        return (f, args, perturbed_output)

    
    #FIXME: add PMX    

    #FIXME: add mutiparent sorting crossover


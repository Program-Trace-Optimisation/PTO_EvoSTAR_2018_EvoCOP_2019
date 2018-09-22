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
       
    
    def blend(self, entry1, entry2):
        return self.PMX(entry1, entry2)
    

    def PMX(self, entry1, entry2):
        
        (typ, output1), (_, output2) = entry1, entry2

        combined_output = output1[:]
        
        size = min(len(output1), len(output2))
        p1, p2 = [0]*size, [0]*size

        # Initialize the position of each indices in the individuals
        for i in range(size):
            p1[output1[i]] = i
            p2[output2[i]] = i
        # Choose crossover points
        cxpoint1 = random.randint(0, size)
        cxpoint2 = random.randint(0, size - 1)
        if cxpoint2 >= cxpoint1:
            cxpoint2 += 1
        else: # Swap the two cx points
            cxpoint1, cxpoint2 = cxpoint2, cxpoint1

        # Apply crossover between cx points
        for i in range(cxpoint1, cxpoint2):
            # Keep track of the selected values
            temp1 = output1[i]
            temp2 = output2[i]
            # Swap the matched value
            combined_output[i], combined_output[p1[temp2]] = temp2, temp1
            # Position bookkeeping
            p1[temp1], p1[temp2] = p1[temp2], p1[temp1]
            p2[temp1], p2[temp2] = p2[temp2], p2[temp1]

        return (typ, combined_output)       

    #FIXME: add mutiparent sorting crossover

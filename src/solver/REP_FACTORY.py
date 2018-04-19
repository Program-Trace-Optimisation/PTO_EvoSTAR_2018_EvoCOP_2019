
import math

#from REP import REP
from REP_INT import INT
from REP_SYM import SYM
from REP_SYM_VECT import SYM_VECT
from REP_PERM import PERM
from REP_REAL import REAL


def REP_factory(entry_type):

    f, args = entry_type
        
    ### INT

    if f.__name__ == "randrange" and len(args) == 1: # random.randrange(stop)
        return INT(0, args[0], 1)

    if f.__name__ == "randrange" and len(args) == 2: # random.randrange(start, stop)
        return INT(args[0], args[1], 1)

    if f.__name__ == "randrange" and len(args) == 3: # random.randrange(start, stop, step)
        return INT(*args)    

    if f.__name__ == "randint": # random.randint(a, b)
        return INT(args[0], args[1]+1, 1) 

    ### SEQ

    if f.__name__ == "choice": # random.choice(seq)
        return SYM(*args)

    #if f.__name__ == "choices": # random.choices(population, weights=None, *, cum_weights=None, k=1)
    #    return SYM_VECT(args[0], k) # FIXME: how do I get k?

    if f.__name__ == "shuffle": # random.shuffle(x[, random])
        return PERM(args[0], len(args[0]))

    if f.__name__ == "sample": # random.sample(population, k)
        return PERM(*args)

    ## REAL

    if f.__name__ == "random": # random.random()
        return REAL(0,1)

    #if f.__name__ == "uniform" and len(args) == 0: # random.uniform()
    #    return REAL(0,1)

    if f.__name__ == "uniform" and len(args) == 2: # random.uniform(a, b)
        return REAL(min(args), max(args))

    if f.__name__ == "triangular": # random.triangular(low, high, mode)
        return REAL(args[0], args[1])

    if f.__name__ == "betavariate": # random.betavariate(alpha, beta)
        return REAL(0, 1)

    if f.__name__ == "expovariate": # random.expovariate(lambd)
        return ( REAL(0, float('inf')) if args[0] >= 0 else REAL(-float('inf'), 0) )

    if f.__name__ == "gammavariate": # random.gammavariate(alpha, beta)
        return REAL(0, float('inf'))

    if f.__name__ == "gauss": # random.gauss(mu, sigma)
        return REAL(-float('inf'), float('inf'))
    
    if f.__name__ == "lognormvariate": # random.lognormvariate(mu, sigma)
        return REAL(0, float('inf'))
    
    if f.__name__ == "normalvariate": # random.normalvariate(mu, sigma)
        return REAL(-float('inf'), float('inf'))
     
    if f.__name__ == "vonmisesvariate": # random.vonmisesvariate(mu, kappa)
        return REAL(0, 2*math.pi)

    if f.__name__ == "paretovariate": # random.paretovariate(alpha)
        return REAL(1, float('inf'))

    if f.__name__ == "weibullvariate": # random.weibullvariate(alpha, beta)
        return REAL(0, float('inf'))
  
    #else:
    return None # fine ops not available, use coarse ops



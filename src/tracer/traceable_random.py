import inspect
from wrapper import make_traceable, random_function

##### WRAP ALL RANDOM FUNCTIONS (AS TERMINALS)

from random import Random

random = Random() # it creates a local random object, rather than changing the random module

for name, fn in inspect.getmembers(random, predicate=inspect.ismethod):
    if name == "shuffle": continue # handle it specially, see below
    #print(name)
    # make random functions both traceable and part of the "runtime" address
    setattr(random, name, random_function(make_traceable(fn)))
setattr(random, 'random', random_function(make_traceable(random.random)))

# Also wrap shuffle specially in order to get both in-place and return
# semantics for shuffle so user can continue to use shuffle in-place
# as usual, but tracer gets a return value in the trace (instead of
# None)

##### FIXME: this degenerates to random search as the address (entry name) and the output are coupled
##### and changing the output changes also the address, so forcing resampling

#random_shuffle_saved = random.shuffle
#def shuffle(x):
#    random_shuffle_saved(x)
#    return x
#setattr(random, 'shuffle', random_function(make_traceable(shuffle)))

#### FIX: we do not allow in-place calls!

random_shuffle_saved = random.shuffle
def shuffle(x):
    y = x[:]
    random_shuffle_saved(y)
    return y
setattr(random, 'shuffle', random_function(make_traceable(shuffle)))

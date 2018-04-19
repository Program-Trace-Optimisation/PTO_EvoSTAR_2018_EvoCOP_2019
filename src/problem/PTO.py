import sys
sys.path.append('../solver')
sys.path.append('../tracer')
sys.path.append('../analysis')

#import random
from solver import solve
from traceable_random import random, random_function #overload module random and use random_function as address decorator
from compare import compare_methods, compare_scalability, compare_all, stat_summary, plot_runs, make_table, plot_scalability

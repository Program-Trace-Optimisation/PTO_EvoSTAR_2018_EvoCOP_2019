from __future__ import print_function

import random as noise # for generating some random problems

# numerical stuff
from math import sqrt
import numpy as np
import itertools

import sys # for CLI

# for file io
import os
import os.path

# for TSPLIB
import gzip

from PTO import random, random_function, solve
from PTO import compare_all, stat_summary, make_table


# Travelling Salesperson Problem.
# An intro to the problem and some basic experimentation is
# available in TSP.ipynb. The experiments in the paper are in
# TSP_experiment.py, which calls this (TSP.py). The results are
# analysed in TSP_results.ipynb.

# no need for @random_function because this will be used as a generator itself
def randsol1(inst):
    # Create a permutation by shuffling. We provide a custom shuffle function.
    return swap_shuffle(range(len(inst)))

@random_function # inform PTO that this function must be traced
def swap_shuffle(perm):
    for i in range(len(perm)):
        ri = random.choice(range(i,len(perm)))
        perm[i],perm[ri]=perm[ri],perm[i]
    return perm

# no need for @random_function because this will be used as a generator itself
def randsol2(inst):
    # Create a permutation by shuffling. We provide a custom shuffle function.
    return rev_shuffle(range(len(inst)))

@random_function # inform PTO that this function must be traced
def rev_shuffle(perm):
    # this is like multiple applications of 2-opt
    for i in range(len(perm)):
        ri = random.choice(range(i,len(perm)))
        perm[i:ri+1] = perm[i:ri+1][::-1] # reverse a section
    return perm


def randsol3(inst):
    """A heuristic generator which takes advantage of problem data in the
    simplest possible way: it chooses from the remaining cities with probabilities
    inversely weighted by distance."""
    n = len(inst)
    sol = []
    remaining = list(range(n))

    # the start city is a decision variable, because we'll get
    # different results if we start at different cities

    x = random.choice(list(range(n))) 

    sol.append(x)
    remaining.remove(x)

    i = 1
    while i < n:

        # choose one of the remaining cities randomly, weighted by
        # inverse distance.
        x = choose_node(inst, x, remaining)
        sol.append(x)
        remaining.remove(x)

        i += 1

    return sol

# no need for @random_function, because choose_node makes no random calls itself
def choose_node(inst, cur, remaining):
    try:
        wts = [1.0 / inst[cur][n] for n in remaining]
    except ZeroDivisionError:
        # if there are two or more nodes with identical locations this
        # can happen. we can just return any of them.
        return [n for n in remaining if inst[cur][n] == 0][0]

    s = sum(wts)
    wts = [wt / float(s) for wt in wts] # normalise

    return roulette_wheel(remaining, wts)

@random_function # inform PTO that this function must be traced
def roulette_wheel(items, wts): # assumes wts sum to 1
    x = random.random()
    for item, wt in zip(items, wts):
        x -= wt
        if x <= 0:
            return item
    # Should not reach here
    print("Error")
    print(items)
    print(wts)
    raise ValueError


# Our fitness function takes an "inst" argument. Fitness is the
# negative of tour length, given a permutation `perm` and a city-city
# distance matrix `inst`.
def fitness(perm, inst):
    # note negative indexing trick to include final step (return to origin)
    return -sum([inst[perm[i-1]][perm[i]] for i in range(0,len(perm))])



# ### Some real TSP instances: TSPLIB
#
# Up to now, we've been generating random TSP instances to demonstrate
# investigation of scalability. Next, we'll read some real TSP
# instances from TSPLIB.
#
# First we get TSPLIB itself. If the following code fails for any
# reason, just download `ALL_tsp.tar.gz` from the given URL, and
# extract it into a new directory `/TSPLIB` in the same directory as
# this notebook.


def get_TSPLIB(dirname):
    import os
    import tarfile
    import requests # conda install requests, or pip install requests

    tsplib_url = "http://www.iwr.uni-heidelberg.de/groups/comopt/software/TSPLIB95/tsp/ALL_tsp.tar.gz"
    r = requests.get(tsplib_url)
    os.makedirs(dirname)
    filename = os.path.join(dirname, "ALL_tsp.tar.gz")
    f = open(filename, "wb")
    f.write(r.content)
    f.close()
    tar = tarfile.open(filename, "r:gz")
    tar.extractall(dirname)
    tar.close()


class TSP:
    def __init__(self, filename):
        self.cities = []
        self.read_file(filename)
        self.matrix = [[self.euclidean_distance(city_i, city_j)
                        for city_i in self.cities]
                       for city_j in self.cities]
        # self.read_optimal_results("TSPLIB/STSP.html")

    def euclidean_distance(self, x, y):
        return sqrt(sum((xi - yi) ** 2.0 for xi, yi in zip(x, y)))

    def read_optimal_results(self, filename):
        # If we would like to look at known optima for these problem see
        # http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/STSP.html. Put
        # that .html file under TSPLIB.
        import re
        optimal_results = {}
        for line in open(filename).readlines():
            p = r">(\w+) : (\d+)<"
            m = re.search(p, line)
            if m:
                key, val = m.group(1, 2)
                key = key.strip()
                # optimal results are given as integers in TSPLIB
                val = int(val.split()[0].strip())
                optimal_results[key] = val
        # print("Optimal results:")
        # print(optimal_results)
        self.optimal = optimal_results[self.name]
        print("Optimum: " + str(self.optimal))

    def read_file(self, filename):
        """FIXME this only works for files in the node xy-coordinate
        format. Some files eg bayg29.tsp.gz give explicit edge weights
        instead."""
        f = gzip.open(filename, "rb")
        coord_section = False
        for line in f.readlines():
            try:
                line = line.strip()
                if line.startswith("NAME"):
                    self.name = line.split(":")[1].strip()
                elif (line.startswith("COMMENT") or
                      line.startswith("TYPE") or
                      line.startswith("EDGE_WEIGHT_TYPE")):
                    pass
                elif line.startswith("DIMENSION"):
                    self.n = int(line.split(":")[1].strip())
                elif line.startswith("NODE_COORD_SECTION"):
                    coord_section = True
                elif line.startswith("EOF"):
                    break
                elif coord_section:
                    # coords are sometimes given as floats in TSPLIB
                    idx, x, y = map(float, line.split())
                    self.cities.append((x, y))
            except:
                print("Filename " + filename)
                print("Error on this line")
                print(line)
                return



# command-line interface: defined by sys.argv usage below.

print(sys.argv)
print("command inst search_algo randsol str_trace budget seed")
source_filename = sys.argv[0]
inst_filename = sys.argv[1]
search_algo = sys.argv[2]
randsol = eval(sys.argv[3])
str_trace = eval(sys.argv[4]) # eval is not dangerous in this context
budget = int(sys.argv[5])
seed = int(sys.argv[6])


TSPLIB_dirname = "TSPLIB"
if not os.path.isfile(os.path.join(TSPLIB_dirname, "att48.tsp.gz")): # example to check if TSPLIB already exists
    get_TSPLIB(TSPLIB_dirname)


inst = TSP(os.path.join(TSPLIB_dirname, inst_filename)).matrix
# specialise the generator and fitness to the instance
_randsol = lambda: randsol(inst)
_fitness = lambda x: fitness(x, inst)

random.seed(seed) # random seed the random module for replicable search behaviour
tour, obj = solve(_randsol, _fitness, solver=search_algo,
                  str_trace=str_trace, budget=budget)
item = (inst_filename, search_algo, randsol.__name__, str_trace, budget, seed, obj, tour)
ofilename = "%s_%s_%s_%d_%d_%d.dat" % (inst_filename, search_algo, randsol.__name__, str_trace, budget, seed)
ofilename = ofilename.replace("/", "_") # in case user has passed in a dirname
ofilename = os.path.join("TSP_results", ofilename)
with open(ofilename, 'w') as outputFile:
    outputFile.write("%s\t%s\t%s\t%d\t%d\t%d\t%f\t%s\n" % item)

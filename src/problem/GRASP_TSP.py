from __future__ import print_function

# numerical stuff
import math
import itertools

import sys # for CLI

# for file io
import os
import os.path

# for TSPLIB
import gzip


# Travelling Salesperson Problem in GRASP-like format as used in our
# EvoCOP paper. Results are analysed in EvoCOP_results.ipynb.

# Note we have another implementation of TSP as used in PPSN 2018, see
# TSP.py.


# Fitness is the
# negative of tour length, given a permutation `perm` and a city-city
# distance matrix `data` (not passed-in).

def fitness(perm):
    # note negative indexing trick to include final step (return to origin)
    return -sum([data[perm[i-1]][perm[i]] for i in range(0,len(perm))])






def empty_solution():
  return []

def complete(solution):
  return len(solution)==n

def allowed_features(solution):
  all_items = range(n) # count from 0 to n-1
  remaining_items = [item for item in all_items if item not in solution]
  return remaining_items

def cost_feature(solution, feat):
  if len(solution) == 0:
    # all cities cost nothing as start city. 
    # NB this will give a uniform random choice of start city,
    # which is better than hardcoding it!
    return 0 
  last_item = solution[-1]
  dist = data[last_item][feat]
  return dist

def add_feature(solution, feat):
  sol = solution[:] + [feat]
  return sol







# Read some real TSP instances from TSPLIB.
#
# First we get TSPLIB itself. If the following code fails for any
# reason, just download `ALL_tsp.tar.gz` from the given URL, and
# extract it into a new directory `/TSPLIB` in the same directory as
# this file.


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
        return math.sqrt(sum((xi - yi) ** 2.0 for xi, yi in zip(x, y)))

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
                line = line.decode()
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


TSPLIB_dirname = "TSPLIB"
if not os.path.isfile(os.path.join(TSPLIB_dirname, "att48.tsp.gz")): # example to check if TSPLIB already exists
    get_TSPLIB(TSPLIB_dirname)

TSPLIB_names = [
    # just a selection of the ones in node xy-coordinate format: the ones we used in PTO paper PPSN 2018
    "att48", "berlin52", "eil101", "u159", "a280", "rat575"
    ]

instances = []
for name in TSPLIB_names:
    inst = TSP(os.path.join(TSPLIB_dirname, name + ".tsp.gz"))
    instances.append({"name": name, "n": len(inst.matrix), "data": inst.matrix})


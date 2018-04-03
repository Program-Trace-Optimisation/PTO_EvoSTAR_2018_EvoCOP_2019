from __future__ import print_function

import os

inst_filenames = [
    "att48.tsp.gz",
    "berlin52.tsp.gz",
    "eil101.tsp.gz",
    "u159.tsp.gz",
    "a280.tsp.gz",
    "rat575.tsp.gz"]



# refuse to overwrite the output file.
odirname = "TSP_results"
assert not os.path.exists(odirname)
os.makedirs(odirname)

nreps = 30
methods = ["RS", "HC", "LA", "EA"]
str_traces = [False, True]
randsols = ["randsol1", "randsol3"]
budget = 20000
nsimul = 10 # eg depending on number of cores

for inst_filename in inst_filenames:
    for method in methods:
        for str_trace in str_traces:
            for randsol in randsols:
                for rep in range(nreps):

                    item = (inst_filename, method, randsol, str_trace, budget, rep)
                    cmd = "python TSP.py %s %s %s %d %d %d" % item

                    if rep % nsimul != nsimul - 1:
                        cmd += " &"
                    print(cmd)
                    os.system(cmd)

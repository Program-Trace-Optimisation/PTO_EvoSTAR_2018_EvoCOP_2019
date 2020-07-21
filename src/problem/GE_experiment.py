from __future__ import print_function

import os
import os.path

# refuse to overwrite the output file.
odirname = "GE_results"
assert not os.path.exists(odirname)
os.makedirs(odirname)

problems = [
    "Pagie2D",
    "DowNorm",
    "HousingNorm",
    "TowerNorm",
    "Vladislavleva4"
    ]

gram_file = "sr.bnf"

nreps = 30
methods = ["RS", "HC", "LA", "EA", "MGA"]
str_traces = [False, True]
randsols = ["GE_randsol_sr_nobnf"]
budget = 20000
nsimul = 15

for problem in problems:
    for method in methods:
        for str_trace in str_traces:
            for randsol in randsols:
                for rep in range(nreps):

                    item = (problem, gram_file, method, randsol, str_trace, budget, rep)
                    cmd = "python GE.py %s %s %s %s %d %d %d" % item

                    if rep % nsimul != nsimul - 1:
                        cmd += " &"
                    print(cmd)
                    os.system(cmd)
                    

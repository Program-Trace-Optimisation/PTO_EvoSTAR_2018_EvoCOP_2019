from PTO import random, solve, random_function

import GRASP_ORDERING, GRASP_KNAPSACK, GRASP_JSSP, GRASP_TSP

import sys, os, math, time

import random as noise


"""

This file is for running experiments for an EvoCOP 2019 submission:

-several combinatorial optimisation problems
-several instances of each problem
-maybe 5 different values of alpha
-several PTO solvers RS, HC, EA
-PTO with versus without a new improved repair method for better re-use of valid outputs.
-multiple repetitions

Running this file will do all of the above. Give command-line
arguments specifying the start and stop values for the random seeds
(thus the number of repetitions), eg ./EvoCOP_experiments.py 0 30 will
do 30 repetitions with seeds 0 - 29.

However this file is written to use a tiny budget of fitness
evaluations, and without writing anything to disk. To use a realistic
budget and write to disk, uncomment appropriate lines at the bottom.

One further complication is that the new improved repair method is implemented as
a "patch" for now. To use it, please run:

$ mv ../tracer/wrapper.py ../tracer/wrapper_nopatch.py; mv ../tracer/wrapper_patch.py ../tracer/wrapper.py

(before starting PTO). To revert, execute the following:

$ mv ../tracer/wrapper.py ../tracer/wrapper_patch.py; mv ../tracer/wrapper_nopatch.py ../tracer/wrapper.py

"""


def GRASP_randsol():
    solution = empty_solution()
    while(not complete(solution)):
        features = allowed_features(solution)
        costs = {feat:cost_feature(solution, feat) for feat in features}
        selected_feature = choose_feature(features, costs, solution, alpha) # only source of randomness
        solution = add_feature(solution, selected_feature)
    return solution

def stepuniform(features, costs, solution, alpha):
    # This implements the RCL as used in GRASP, which is a
    # step-uniform distribution In this version, alpha gives a
    # threshold on cost. This is the only type used in the EvoCOP
    # paper.
    min_cost, max_cost = min(costs.values()), max(costs.values())
    RCL = [feat for feat in features if costs[feat] <= min_cost + alpha * (max_cost - min_cost)]
    return random.choice(RCL)

def stepuniformrank(features, costs, solution, alpha):
    # This implements the RCL as used in GRASP which is a step-uniform
    # distribution In this version, alpha gives a threshold on ranked
    # cost.
    features.sort(key=lambda feature: costs[feature], reverse=True) # FIXME I considered quick-select but didn't find it clearly faster for typical workload, but this could be revisited.
    threshold = int(alpha * len(features))
    idx = random.randrange(threshold) # FIXME does this method preserve the trace?
    return features[idx]

def triangularrank(features, costs, solution, alpha):
    # This implements a triangular distribution as in some Juan et al
    # work. The pdf has a peak at 0 and scales linearly to 0 at alpha
    # * n
    n = len(features)
    # FIXME does this method preserve the trace correctly?
    r = random.triangular(0, alpha * n, 0) # LB, UB, mode
    idx = int(r)
    if idx >= n: # very rare, the equivalent of sampling 1.0 from a uniform on [0.0, 1.0]
        idx -= 1   # it would choose an invalid feature, so we hack it.
    features.sort(key=lambda feature: costs[feature], reverse=True) # FIXME see above re quick-select
    return features[idx]

    
dirname = "EvoCOP_results"
os.makedirs(dirname, exist_ok=True)
problems = [GRASP_ORDERING, GRASP_JSSP, GRASP_KNAPSACK, GRASP_TSP]
distributions = [stepuniform]
alpha_vals = [0.0, 0.1, 0.5, 0.9, 1.0]
solvers = ["RS", "HC", "EA"]
str_trace_vals = [True]
# patch_vals = [False] # mv ../tracer/wrapper.py ../tracer/wrapper_patch.py; mv ../tracer/wrapper_nopatch.py ../tracer/wrapper.py
patch_vals = [True]  # mv ../tracer/wrapper.py ../tracer/wrapper_nopatch.py; mv ../tracer/wrapper_patch.py ../tracer/wrapper.py

budget = 200 # Change to 20,000 for the results as in the paper.
start_rep, end_rep = int(sys.argv[1]), int(sys.argv[2])

for problem in problems:
    for instance in problem.instances:
        print(instance["name"])

        # make all the instance information available to the problem module
        setattr(problem, "instance", instance)
        for k in instance:
            setattr(problem, k, instance[k])

        fitness = problem.fitness
        empty_solution = problem.empty_solution
        complete = problem.complete
        allowed_features = problem.allowed_features
        cost_feature = problem.cost_feature
        add_feature = problem.add_feature
        for choose_feature in distributions:
            for alpha in alpha_vals:
                for solver in solvers:
                    for patch in patch_vals:
                        for str_trace in str_trace_vals:
                            for rep in range(start_rep, end_rep):
                                random.seed(rep)
                                noise.seed(rep)
                                fname = "_".join(map(str, [problem.__name__, instance["name"], instance["n"], choose_feature.__name__, alpha, solver, patch, str_trace, budget, rep]))
                                full_fname = dirname + "/" + fname + ".dat"

                                # if running in a multi-core
                                # environment with stopping and
                                # restarting of the script, this line
                                # helps avoid re-running setups
                                # already finished.
                                if os.path.exists(full_fname):
                                    continue

                                # do the run! (and time it)
                                start_time = time.time()
                                ind, fit = solve(GRASP_randsol, fitness, solver=solver, str_trace=str_trace, budget=budget)
                                end_time = time.time()
                                elapsed_time = end_time - start_time
                                
                                output = "\t".join(map(str, [problem.__name__, instance["name"], instance["n"], choose_feature.__name__, alpha, solver, patch, str_trace, budget, rep, start_time, elapsed_time, fit, str(ind)]))
                                print(output)
                                # uncomment this line to write to disk.
                                # open(full_fname, "w").write(output + "\n")

from PTO import random, solve, random_function

import GRASP_ORDERING, GRASP_KNAPSACK, GRASP_JSSP, GRASP_TSP

import sys, math, time


"""

This file is for running experiments:

-several combinatorial optimisation problems
-several instances of each problem
-a GRASP-in-PTO approach, and a biased randomisation-in-PTO approach
 (both implemented as GRASP with different distributions)
-maybe 5 different values of alpha
-several PTO solvers RS, HC, EA
-PTO linear versus structured trace
-PTO with versus without a patch for re-use of valid outputs,

Biased Randomisation can be seen as a generalisation of the main idea
of GRASP. Instead of choosing uniformly from the restricted candidate
list, it can choose from all possible candidates according to any
distribution. For example, we may use a triangular or exponential
distribution. See "MIRHA: multi-start biased randomization of
heuristics with adaptive local search for solving non-smooth routing
problems" (Juan et al., p. 121).


"""

def GRASP_randsol():
    solution = empty_solution()
    while(not complete(solution)):
      features = allowed_features(solution)
      costs = {feat:cost_feature(solution, feat) for feat in features}
      selected_feature = choose_feature(features, costs, solution, alpha) # only source of randomness
      solution = add_feature(solution, selected_feature)
    return solution

def step_uniform(features, costs, solution, alpha):
    # This implements the RCL as used in GRASP
    # which is a step-uniform distribution
    min_cost, max_cost = min(costs.values()), max(costs.values())
    RCL = [feat for feat in features if costs[feat] <= min_cost + alpha * (max_cost - min_cost)]
    return random.choice(RCL)

def triangular(features, costs, solution, alpha):
    # a triangular distribution: pdf has a peak at 0 and scales linearly to 0 at alpha * n
    n = len(features)
    r = random.triangular(0, alpha * n, 0) # LB, UB, mode
    idx = int(r)
    # print("alpha, n, r, idx", alpha, n, r, idx)
    if idx >= n: # very rare, the equivalent of sampling 1.0 from a uniform on [0.0, 1.0]
      idx -= 1   # it would choose an invalid feature, so we hack it.
    features.sort(key=lambda feature: costs[feature], reverse=True) # FIXME consider quick-select
    return features[idx]

# @random_function
# def choose_from_Boltzmann(features, costs, solution, alpha):
#     # a Boltzmann distribution: alpha controls how "peaked" the distribution is near 0
#     n = len(features)
#     minp, maxp = -2, 1
#     lambda_ = 10**(maxp - alpha * (maxp - minp)) / math.log10(n + 1)
#     idx = boltzmann.rvs(lambda_, n, size=1)[0] # FIXME would need to trace this
#     features.sort(key=lambda feature: costs[feature], reverse=True) # FIXME consider quick-select
#     return features[idx]


problems = [GRASP_ORDERING, GRASP_JSSP, GRASP_KNAPSACK, GRASP_TSP]
# problems = [GRASP_KNAPSACK]
distributions = [step_uniform, triangular]
alpha_vals = [0.0, 0.5, 1.0]
# alpha_vals = [1.0]
solvers = ["RS", "HC", "EA"]
# solvers = ["HC"]
str_trace_vals = [False, True]
patch_vals = [False] # we'll have to hardcode this for now: run EvoCOP_experiments.py twice, once with wrapper.py and once with wrapper_patch.py. Set this val here for bookkeeping
budget = 5
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
        # for patch in [True, False]:
        for choose_feature in distributions:
            for alpha in alpha_vals:
                for solver in solvers:
                    for patch in patch_vals:
                        for str_trace in str_trace_vals:
                            for rep in range(start_rep, end_rep):
                                start_time = time.time()
                                ind, fit = solve(GRASP_randsol, fitness, solver=solver, str_trace=str_trace, budget=budget)
                                end_time = time.time()
                                elapsed_time = end_time - start_time
                                print(problem.__name__, instance["name"], instance["n"], choose_feature.__name__, alpha, solver, str_trace, rep, start_time, elapsed_time, fit, str(ind))

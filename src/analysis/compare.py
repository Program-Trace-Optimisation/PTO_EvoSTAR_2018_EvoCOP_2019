from __future__ import print_function

from solver import solve

from functools import partial
from collections import defaultdict

try:
    import numpy as np
    import scipy.stats
    import matplotlib.pyplot as plt
except:
    print("Warning: Numpy, Scipy, or Matplotlib cannot be imported, so no analysis available during this run (maybe you are using pypy?)")
    

from pprint import pprint

# quick text-mode report on a statistical distribution
def stat_summary(x):
    return "mean %.2f std %.2f min %.2f med %.2f max %.2f" % (
        np.mean(x), np.std(x), np.min(x), np.median(x), np.max(x))

# compare solvers (ie search methods) over multiple runs on a fixed
# problem.
def compare_methods(solgen, fitness, term=2, num_runs=10, init=None):
    data = []
    for met in ["RS", "HC", "LA", "EA", "PS"]:
        fits = []
        for _ in range(num_runs):
            if init != None: init()
            fits.append(solve(solgen, fitness, solver=met, effort=term)[1])
        #fits = map(fitness, sols) # does not work with non-static fitness
        min_fit = min(fits)
        avg_fit = reduce(lambda x,y:x+y,(fits))/float(len(fits))
        max_fit = max(fits)
        #print(met, " - best: ", min(fits), "avg: ", float(sum(fits))/len(fits))
        data.append((min_fit, avg_fit, max_fit))
    return data


# compare everything: sizes, structured v unstructured trace,
# generators, solvers, and return a dict of results, keyed by
# (size, trace, generator name, solver)
def compare_all(fitness,
                solgens,
                sizes=None,
                random_instance=None, # a function to generate a random instance, assumed to take a size argument
                instances=None,
                methods=None,
                str_traces=None,
                budget=10000,
                num_runs=10,
                print_progress=False):

    if methods is None: methods = ["HC"]
    if str_traces is None: str_traces = [True]

    # can't have both sizes and instances
    assert (sizes is None) + (instances is None) > 0

    # instances will be a dict mapping rep number to a list of instances
    if instances is None:
        if sizes is None:
            instances = {rep: [None] for rep in range(num_runs)}
            problem_ids = [None]
        else:
            if random_instance:
                instances = {rep: [random_instance(size) for size in sizes]
                             for rep in range(num_runs)}
                problem_ids = sizes
            else:
                instances = {rep: sizes for rep in range(num_runs)}
                problem_ids = sizes

    else:
        instances = {rep: instances for rep in range(num_runs)}
        problem_ids = instances

    results = defaultdict(list)

    # for rep, for inst, for trace, for solgen, for method
    for rep in range(num_runs):

        for problem_id, inst in zip(problem_ids, instances[rep]):

            if inst is None:
                fitness_inst = fitness
            else:
                fitness_inst = lambda x: fitness(x, inst) # can't use partial: wrong ordering of args
                fitness_inst.__name__ = fitness.__name__

            for str_trace in str_traces:
                for solgen in solgens:

                    if inst is None:
                        solgen_inst = solgen
                    else:
                        solgen_inst = partial(solgen, inst)
                        solgen_inst.__name__ = solgen.__name__

                    for method in methods:

                        key = (problem_id, str_trace, solgen.__name__, method)
                        ind, fit = solve(solgen_inst, fitness_inst,
                                         solver=method, budget=budget,
                                         str_trace=str_trace)
                        results[key].append(fit)
                        if print_progress: print(rep, key, fit)
    return results




# plot scalability. Assumes that results has been created by compare_all.
def plot_scalability(results):
    sizes = sorted(set(k[0] for k in results.keys()))
    trace_types = sorted(set(k[1] for k in results.keys()))
    generators = sorted(set(k[2] for k in results.keys()))
    methods = sorted(set(k[3] for k in results.keys()))

    # there should be exactly zero or one of these with more than 1 option, to be plotted
    assert (len(trace_types) > 1) + (len(generators) > 1) + (len(methods) > 1) <= 1

    if len(methods) > 1:
        for method in methods:
            plt.plot(sizes, [np.mean(results[(size, trace_types[0], generators[0], method)]) for size in sizes])
        plt.legend(methods, loc='lower right')
    elif len(generators) > 1:
        for generator in generators:
            plt.plot(sizes, [np.mean(results[(size, trace_types[0], generator, methods[0])]) for size in sizes])
        plt.legend(generators, loc='lower right')
    elif len(trace_types) > 1:
        for trace_type in trace_types:
            plt.plot(sizes, [np.mean(results[(size, trace_type, generators[0], methods[0])]) for size in sizes])
        plt.legend(trace_types, loc='lower right')
    else:
        plt.plot(sizes, [np.mean(results[(size, trace_types[0], generators[0], methods[0])]) for size in sizes])
        # no legend needed

    plt.ylabel("Fitness")
    plt.xlabel("Problem size")
    plt.show()

# Carry out some runs and plot results (objective versus iterations)
def plot_runs(randsol, fitness, methods=None, budget=1000, num_runs=5):
    if methods is None: methods = ["RS", "HC", "LA", "EA", "PS"]

    for method in methods:
        results = []
        for run in range(num_runs):
            ind, fit = solve(randsol, fitness, solver=method, budget=budget)
            results.append(solve.data)
        results = np.array(results)
        plt.plot(np.mean(results, axis=0))
    plt.legend(methods, loc='lower right')
    plt.xlabel("Fitness evaluations")
    plt.ylabel("Fitness")
    plt.show()

# prints a nicely-formatted text-mode table with the results from compare_all
def make_table(results):
    # assumes results contains multiple runs, per key
    for key in sorted(results.keys()):
        print(str(key) + ": " + stat_summary(results[key]))


# generate_problems_at_sizes is for the case where at any problem size
# we can generate some problem instance(s). The idea is to generate
# the instances with this, and pass them to compare_all.
def generate_problems_at_sizes(randsol, fitness, min_size, max_size, randinst=None):
    for i in range(min_size, max_size):
        if randinst:
            inst = randinst(i)
            yield partial(randsol, inst), partial_fitness(randsol, inst)
        else:
            yield partial(randsol, i), partial_fitness(randsol, i)


# compare scalability. This expects randsol and fitness to have a
# keyword parameter called problem_size
def compare_scalability(rsol, fit, min_size, max_size, num_runs=10, term=2):
    data = {}
    for size in range(min_size, max_size):
        print(".", end="")
        data[size] = compare_methods(partial(rsol, problem_size=size), partial(fit, problem_size=size), num_runs=num_runs, term=term)
    for method in ["RS", "HC", "EA", "PS"]:
        plt.plot([data[size][method][2] for size in range(min_size,max_size)])
    plt.legend(["RS", "HC", "EA", "PS"], loc='lower right')
    plt.title("solution quality vs problem size")
    plt.show()

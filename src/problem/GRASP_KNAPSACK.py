import random
import pprint

# TODO
# try to use generator expressions everywhere there's a list below to save memory
# also solution.append(feat) instead of solution[:], for speed


def fitness(solution):
    return sum([val[item] for item in solution])



def empty_solution():
    return []  

def complete(solution):
    weight = sum([wt[item] for item in solution])
    min_weight_left = min([wt[item] for item in range(n) if item not in solution])
    return len(solution)==n or (weight + min_weight_left) > W

def allowed_features(solution):
    all_items = range(n)
    remaining_items = [item for item in all_items if item not in solution]
    weight = sum([wt[item] for item in solution])
    fitting_items = [item for item in remaining_items if (weight + wt[item]) <= W]
    return fitting_items

def cost_feature(solution, feat):
    return -val[feat] # heuristic 1 (-val as this is a cost)
    #return -val[feat]/wt[feat] # heuristic 2

def add_feature(solution, feat):
    sol = solution[:] + [feat]
    return sol




toy_instances = [
    {"name": "test-Knapsack-3", "n": 3,
     "val": [60, 100, 120], "wt": [10, 20, 30], "W": 50}
]

filename = "knapsack-random-instances-PTO.dat"
instances = eval(open(filename).read())

def random_instance(n):
    return {
        "name": "knapsack-random-instance-PTO-%d" % n,
        "doc": "Randomly-generated one-dimensional Knapsack instance. Generated using https://github.com/Program-Trace-Optimisation/PTO/blob/master/src/problem/GRASP_KNAPSACK.py with Python 3, random seed 0, on 5 Nov 2018. We use contiguous integer values for the weights so that they are well spread-out and the solution will consist of at least several items, not just 1 or 2. It is suggested to read this file in using eval(open(filename).read()).",
        "n": n,
        "val": [random.randint(1,100) for i in range(n)],
        "wt": list(range(1,n+1)),
        "W": 2*n
        }

def generate_and_write_random_instances():
    """Running this script will generate some random instances and save them to a file.
    We'll use a random seed of 0 so that people can re-generate if needed
    for replicability. But the file itself can also be distributed."""
    random.seed(0)
    insts = []
    sizes = [10, 20, 40, 80, 160, 320]
    for n in sizes:
        inst = random_instance(n)
        insts.append(inst)
    pp = pprint.PrettyPrinter(indent=1, stream=open(filename, "w"))
    pp.pprint(insts)


if __name__ == "__main__":
    generate_and_write_random_instances()

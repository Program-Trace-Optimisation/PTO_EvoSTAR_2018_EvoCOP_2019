def fitness(solution):
    return -sum([val[item] for item in solution])





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




instances = [
    {"name": "test-Knapsack-3", "n": 3,
     "val": [60, 100, 120], "wt": [10, 20, 30], "W": 50}
]


def random_instance(n):
    return {
        "name": "random-Knapsack-%d" % n,
        "n": n,
        "val": [random.randint(1,100) for i in range(n)],
        "wt": list(range(1,n+1)),
        "W": 2*n
        }



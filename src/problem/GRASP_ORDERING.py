def fitness(solution): # cost to minimise, best solution has cost 0
    return -sum([abs(solution[pos]-(pos+1)) for pos in range(n)])



def empty_solution():
    return []

def complete(solution):
    return len(solution)==n

def allowed_features(solution):
    all_items = range(1,n+1)
    remaining_items = [item for item in all_items if item not in solution]
    return remaining_items

def cost_feature(solution, feat):
    last_item = solution[-1] if len(solution)>0 else 0
    dist = abs(feat - last_item)
    return dist

def add_feature(solution, feat):
    sol = solution[:] + [feat]
    return sol




instances = [
    {"name": "ordering-10", "n": 10},
    {"name": "ordering-20", "n": 20},
    {"name": "ordering-40", "n": 40},
    {"name": "ordering-80", "n": 80},
    {"name": "ordering-160", "n": 160},
    {"name": "ordering-320", "n": 320},
]


def random_instance(n):
    return {"name": "ordering-%d" % n, "n": n}
  

#from __future__ import print_function

from PTO import random, solve, compare_methods #, compare_scalability #random_function


##### ONE MAX #####


##### 1) define your random solution generator

n=30

#@random_function
def randsol1(problem_size=n):
    #return random.sample([0,1,2,3],4) 
    #return [random.choice([0,1]) for x in range(problem_size)]
    #return [random.uniform(0,1) for x in range(problem_size)]
    return [random.randrange(5) for x in range(problem_size)]

#print(randsol1())

#def randsol(problem_size=n):
#    return solve(randsol1, fitness, solver = "HC", budget = 10)[0]

##### 2) define your fitness function

def fitness(string, problem_size=n):
    return sum(string) # we are maximising

#print(solve(randsol1, fitness, solver = "HC", effort = 1))

rs = randsol1()
print("R :", (rs, fitness(rs)))

##### 3) optimize it!

for method in ["RS", "HC", "LA", "EA", "PS", "MGA"]:
    for trace_type in [False, True]:
        print(method, trace_type)
        print(solve(randsol1, fitness, solver = method, str_trace = trace_type, fine_ops=True, effort = 2))



##### 4) ... and analyze it


# methods

print(compare_methods(randsol1, fitness, num_runs=10, term=2))
# min, avg fitness of 10 runs of RS, HC, EA, PS


# scalability

#compare_scalability(randsol, fitness, 4, 20)
# expects randsol and fitness to have a keyword parameter called problem_size




######################################################

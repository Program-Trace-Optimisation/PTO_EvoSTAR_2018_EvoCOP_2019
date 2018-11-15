import random
import os.path
import re
import io


# Get a file of instances from OR library

url = "http://people.brunel.ac.uk/~mastjjb/jeb/orlib/files/jobshop1.txt"
filename = url.split("/")[-1]
if not os.path.exists(filename):
  import requests # conda install requests, or pip install requests
  
  r = requests.get(url)
  f = open(filename, "wb")
  f.write(r.content)

txt = open(filename).read()

name = r" instance (\w*)\n.*?"
blank = r"\n"
plusses = r".\+\+\+\+\+\+\+\+\+\+\+\+\+\+.*?\n"
desc = r".*?\n"
size = r" (\d+) (\d+)\n"
data = r"(.*?)"
pattern = name + blank + plusses + desc + size + data + plusses

def convert_problem_data(inst_data):
    # read to numpy from a string
    data = []
    for line in inst_data.split("\n"):
        line = list(map(int, line.split()))
        data.append(line)
    problem = []
    # convert each instance to a list of lists of pairs, where each pair
    # gives (machine, time needed)
    for line in data:
        i = 0
        job = []
        while i < len(line):
            job.append((line[i], line[i+1]))
            i += 2
        problem.append(job)
    return problem

# There are many instances in the jobshop1.txt file but we take just these 6
# for EvoCOP experiments.
instance_names = [
  "abz5",
  "abz6",
  "abz7",
  "abz8",
  "abz9",
  "yn1"
  ]

instances = []

for inst_name, n, m, inst_data in re.findall(pattern, txt, flags=re.DOTALL):
  #print(inst_name)
  if inst_name in instance_names:
    instances.append({"size": (n, m),
                      "data": convert_problem_data(inst_data),
                      "name": inst_name,
                      "n": n,
                      "m": m})
  

def fitness(solution): # makespan: maximum of termination times on machines
    # PTO always maximises, but we want small makespan, so use -max
    return -max([solution[mac][-1][2] for mac in solution])

# Other possible objectives exist, eg total weighted tardiness, see EJOR 2017 paper





def empty_solution():
    # Global variables keep track of the schedule under construction
    global jobs, machines, term_mac, term_job
    jobs = [list(job) for job in instance["data"]]
    machines = {} # dictionary of machines
    term_mac = {} # termination times on machines
    term_job = {} # termination times of jobs
    
    return {}

def complete(solution):
    #print(solution)
    return all(job == [] for job in jobs)

def allowed_features(solution):
    job_inds = [ i for i in range(len(jobs)) if jobs[i] != [] ]
    #print(job_inds)
    return job_inds

def cost_feature(solution, feat):
    makespan = max([solution[mac][-1][2] for mac in solution]) if solution != {} else 0

    op = jobs[feat][0]
    if ((feat not in term_job) or (op[0] not in term_mac)):
        term_op = op[1]
    else:
        term_op = max(term_job[feat],term_mac[op[0]])+op[1]

    #print(term_op - makespan)
    return term_op - makespan

def add_feature(solution, feat):
    op, jobs[feat] = jobs[feat][0], jobs[feat][1:]

    if (feat not in term_job):
        term_job[feat] = 0 # initialise dictionary
    if (op[0] not in term_mac):
        term_mac[op[0]] = 0 # initialise dictionary

    term_op = max(term_job[feat],term_mac[op[0]])+op[1]
    term_job[feat]=term_op
    term_mac[op[0]]=term_op

    #machines = solution.copy()
    if op[0] not in machines: # if machine of current operation not in dictionary
        machines[op[0]] = [(feat, op[0], term_op)] # for each op: (job, mac, term)
    else:
        machines[op[0]].append((feat, op[0], term_op))

    return machines





# Each sub-list is a job (a sequence of operations).
# Each pair gives the machine the operation has to be processed on, and the time it takes.

# 3 jobs, 3 machines

toy_instances = [
  [[(0,3), (1,2), (2,2)],
   [(0,2), (2,1), (1,4)],
   [(1,4), (2,3)]]
]

def random_instance(n, m): # n jobs on m machines
    prob = []
    for i in range(n):
        nmachines = random.randrange(1, m+1)
        machines = random.sample(range(m), nmachines)
        job = [(machine, (1 + random.randrange(1,5))*10)
               for machine in machines]
        prob.append(job)
    return prob

# instance = randprob(4, 6)
# print(instance)





from __future__ import print_function

# PTO stuff
from PTO import random, random_function, solve
import grammar
import random as noise # for generating some random problems

# numerical stuff
from math import sqrt
import numpy as np
import itertools

# for file io
import os
import os.path
import sys

# We define the arithmetic functions we'll use as primitives in the
# grammar.
def add(x, y): return x + y
def sub(x, y): return x - y
def mul(x, y): return x * y
# aq is the analytic quotient from: Ji Ni and Russ H. Drieberg and
# Peter I. Rockett, "The Use of an Analytic Quotient Operator in
# Genetic Programming", IEEE Transactions on Evolutionary Computation
def aq(x, y):  return x/np.sqrt(1.0+y*y)


# Next, we define a generator suitable for GE: it generates a random
# string by derivation from a grammar, then turns that into a
# function.
def GE_randsol(gram):
    s = random_str(gram, None)
    f = eval("lambda x:" + s)
    f.func_name = s
    return f

@random_function # essential    
def random_str(grammar, s=None):
    """Recursively derive a random string given a grammar. Don't create a
    derivation tree."""
    if s is None:
        s = grammar.start_rule[0]
    elif s in grammar.terminals:
        return s
    rule = grammar.rules[s]
    if len(rule) > 1:
        prod = random.choice(rule)
    else:
        prod = rule[0]
    return "".join([random_str(grammar, s[0]) for s in prod])

# Our grammar is implemented as an "executable" below, but is equivalent
# to the following BNF:
"""    
<expr> ::= <op>(<expr>, <expr>) | <var> | <const>
<op> ::= add | sub | mul | aq
<var> ::= x[<varidx>]
<varidx> ::= GE_RANGE:n_vars
<const> ::= 0.0 | 0.1 | 0.2 | 0.3 | 0.4 | 0.5 | 0.6 | 0.7 | 0.8 | 0.9 | 1.0
"""

def GE_randsol_sr_nobnf():
    s = Expr()
    f = eval("lambda x:" + s)
    f.func_name = s
    return f
    
RC = random.choice

@random_function
def Expr(): return RC([Op_Expr_Expr, Var, Const])()

@random_function
def Op_Expr_Expr(): return Op() + "(" + Expr() + ", " + Expr() + ")"

@random_function
def Op(): return RC(["add", "sub", "mul", "aq"])

@random_function
def Var(): return "x[" + str(random.randrange(n_vars)) + "]"

@random_function
def Const(): return RC(["0.0", "0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "1.0"])



# Now we define an objective function. There is a target function (eg
# Pagie 2D, or a randomly-generated polynomial). We'll define the
# objective as -RMSE (since in PTO, higher is better).
def fitness_sr_data(X, y):
    def f(individual):
        'Determine the fitness of an individual as -RMSE. Higher is better.'
        try:
            yhat = individual(X)
            rmse = np.sqrt(np.mean((y - yhat) ** 2))
        except (ZeroDivisionError, TypeError) as e:
            print(e)
            rmse = 1.0e20
        return -rmse
    return f
    

def fitness_sr(target, train_X="random"):
    # random fitness cases in the [-1, 1] hypercube
    if type(train_X) == str and train_X == "random":
        train_X = [tuple([2*(noise.random() - 0.5) for j in range(target.n_vars)]) for i in range(20)]
    train_y = target(train_X)

    ones = np.ones_like(train_y)

    def f(individual):
        'Determine the fitness of an individual as -RMSE. Higher is better.'

        try:
            yhat = individual(train_X)
            rmse = np.sqrt(np.mean((train_y - yhat) ** 2))
        except (ZeroDivisionError, TypeError) as e:
            print(e)
            rmse = 1.0e20
        return -rmse
    return f


def read_data(filename):
    d = np.genfromtxt(filename, skip_header=1, delimiter="\t").T
    return d[:-1], d[-1]



# command-line interface: defined by the below sys.argv usage

source_filename = sys.argv[0]
problem = sys.argv[1]
gram_file = sys.argv[2]
search_algo = sys.argv[3]
randsol = eval(sys.argv[4])
str_trace = eval(sys.argv[5]) # eval is not dangerous in this context
budget = int(sys.argv[6])
seed = int(sys.argv[7])

# random seed the random module for replicable
# search behaviour. also replicable random generation of the polynomial
# target if any, and fitness cases
random.seed(seed)
noise.seed(seed)
np.random.seed(seed)


if problem.startswith("poly_"):
    import polynomial
    deg, n_vars = map(int, problem.split("_")[1:])
    coefs = [2*(noise.random() - 0.5) for i in polynomial.Polynomial.terms(deg, n_vars)]
    p = polynomial.Polynomial(deg, n_vars, coefs)
    nrows = 20
    train_X = np.random.random((n_vars, nrows))
    fitness = fitness_sr(lambda x: p.eval(x), train_X=train_X)
    test_fitness_fn = fitness # no separate training set
else:
    train_X, train_y = read_data(os.path.join("datasets", problem, "Train.txt"))
    test_X, test_y = read_data(os.path.join("datasets", problem, "Test.txt"))
    n_vars = train_X.shape[0]
    fitness = fitness_sr_data(train_X, train_y)
    test_fitness_fn = fitness_sr_data(test_X, test_y)

# Special case when randsol is GE_randsol_sr_nobnf: there is no .bnf file
if sys.argv[4].endswith("nobnf"):
    _randsol = randsol
else:
    gram = grammar.Grammar(file_name=gram_file, n_vars=n_vars)
    _randsol = lambda: randsol(gram)


fn, obj = solve(_randsol, fitness, solver=search_algo, str_trace=str_trace, budget=budget)

test_obj = test_fitness_fn(fn)

item = (problem, gram_file, search_algo, randsol.__name__, str_trace, budget, seed, obj, test_obj, fn.__name__)
ofilename = "%s_%s_%s_%s_%d_%d_%d.dat" % item[:-3]
ofilename = ofilename.replace("/", "_") # in case user has passed in a dirname
ofilename = os.path.join("GE_results", ofilename)
open(ofilename, "w").write("%s\t%s\t%s\t%s\t%d\t%d\t%d\t%f\t%f\t%s\n" % item)

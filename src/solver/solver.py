######################### STRUCTURED TRACE SOLVERS #########################

from __future__ import print_function

import math

from tracer import tr
from search_operators import OPS  

solver_name = {
	"RS" : "random_search_class",
	"HC" : "hill_climber_class",
	"LA" : "lahc_class",
	"EA" : "evolutionary_algorithm_class",
	"PS" : "particle_swarm_class"
}



def solve(randsol, fitness, solver=None, budget=None, effort=1.5, fine_ops=False, str_trace=True):

    ##### PARAMETERS

    ### set the tracer object 
    tr.set_str_addr(str_trace)

    ### create an instance of the search operators
    ops = OPS(randsol, fitness, fine_ops, tr)

    ##### BUDGET AND EFFORT
    if not budget:
        # If budget is given, use that to determine the iteration
        # budget.  This allows us to specify the number of iterations
        # directly, which is useful for fair benchmarking. Otherwise,
        # estimate genotype size and calculate budget.
        # GENO_SIZE = int(sum([len(ops.create_ind()[1]) for _ in range(100)])/100.0)
        # print(randsol())
        # print(ops.create_trace()[1])
        # print("GENO_SIZE" + str(GENO_SIZE))
        # print("computing budget ", end="")
        budget = int(ops.avg_size_ind() ** effort)
        # print(" budget = ", budget)

    #return
    
    ##### SOLVER

    if solver in solver_name:

    #if solver == "RS":
		
        #### import solver module 	
        solver_module = __import__(solver_name[solver])

        #### get solver class
        Solver_Class = getattr(solver_module, solver) # assumes class name same as solver acronym

        #### create an instance of the solver
        search_algorithm = Solver_Class(ops, budget)
	
        #### run the solver
        ((pheno, _), found_fit) = search_algorithm.run()
	
        #### collect data
        solve.data = search_algorithm.data
    
        #### return solution
        return (pheno, found_fit)
	
    else:
	
        print("solver %s not available!" % solver)
        print("solver = RS | HC | LA | EA | PS")
    
    
    
################################################################################

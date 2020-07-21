
######################### SOLVER #########################

import math

from tracer import Tracer
from wrapper import wr
from search_operators import OPS
from AUTO_PARAM import avg_size_trace

#FIX ME: get all solver names automatically 
solver_name = {
	"RS" : "ALG_RS_random_search",
	"HC" : "ALG_HC_hill_climber",
	"LA" : "ALG_LAHC_late_acceptance",
	"EA" : "ALG_EA_evolutionary_algorithm",
	"PS" : "ALG_PS_particle_swarm",
	"MGA": "ALG_MGA_microbial_genetic_algorithm"
}


def solve(randsol, fitness, solver=None, budget=None, effort=1.5, fine_ops=True, str_trace=True):

	##### PARAMETERS
	
	### create a tracer object
	tr = Tracer(rs=randsol, tt=str_trace) 

	### associate wrapper and tracer
	tr.acquire_wrapper(wr)
	
	### create an instance of the search operators
	ops = OPS(fitness, fine_ops, tr)

	##### BUDGET AND EFFORT
	if not budget:
		# If budget is given, use that to determine the iteration
		# budget.  This allows us to specify the number of iterations
		# directly, which is useful for fair benchmarking. Otherwise,
		# estimate genotype size and calculate budget.
		budget = int(avg_size_trace(tr) ** effort) 
		# print(" budget = ", budget)
    
	##### SOLVER

	if solver in solver_name:
		
		#### import solver module 	
		solver_module = __import__(solver_name[solver])

		#### get solver class
		Solver_Class = getattr(solver_module, solver) # assumes class name same as solver acronym

		#### create an instance of the solver
		search_algorithm = Solver_Class(ops, budget)

		#### run the solver
		(sol, fit) = search_algorithm.run() 
	
		#### collect data
		solve.data = search_algorithm.data
		
		#### release wrapper
		tr.release_wrapper(wr)
    
		#### return solution
		return (sol.pheno, fit) 
	
	else:
	
		print("solver %s not available!" % solver)
		print("solver = RS | HC | LA | EA | PS | MGA")
  
    
################################################################################


	

import inspect
from collections import defaultdict, OrderedDict, Sequence
import itertools
import os

########################## TRACER ##########################

class Tracer:
    """ Tracer """

    def __init__(self, rs = None, tt = True):

        #self.randsol = rs
        self.randsol = lambda: rs() # assocaite random solution generator to tracer
                                    # lambda handles the case of generator decorated with @random_function
                                    # FIXME?: if randsol is not wrapped by @random_function, wrap it. This makes the runtime address uniform. 
                
        self.str_addr = tt
        self.reset_tracer() # initialise state variables

    ##### WRAPPER METHODS

    def acquire_wrapper(self, wr):
        self.prev_tr = wr.tr # save previous tracer associated with wrapper
        wr.tr = self # associate wrapper to current tracer
        #self.randsol = wr.fix_generator(self.randsol)
        #print("acquired wrapper")        
		
    def release_wrapper(self, wr):
        wr.tr = self.prev_tr # resume previous tracer in the wrapper
        #print("released wrapper")		


    ##### TRACE METHODS

    def reset_tracer(self):

        self.mode = "off"
        self.trace = OrderedDict() # {}
        self.new_trace = OrderedDict() # {}
        self.stack = []
        self.multiple = [] #[defaultdict(int)]


    def get_trace(self):

        self.reset_tracer()
        self.mode = "trace" #start tracing
        rs = self.randsol() #generate sample and trace
        self.mode = "off" #stop tracing

        #print(trace)
        return (rs, self.trace) #(pheno, geno)


    def play_trace(self, input_trace):

        self.reset_tracer()
        self.mode, self.trace = "play", input_trace #set trace to input trace and play it from the beginning
        rs = self.randsol() #regenerate sample corresponding to input trace if possible, or fix trace
        self.mode = "off" #stop tracing

        return (rs, self.new_trace) #(pheno, geno)


    ##### TRACE DISPLAY

    # FIXME: this should be part of Trace class?

    def display_trace(self, trace):

        for k in trace.keys():
            (f, args), output = trace[k]
            print(k, "---->", f.__name__ + str(args) + " = " + str(output))






import inspect
from collections import defaultdict, OrderedDict, Sequence
import itertools
import os

########################## TRACER ##########################

class Tracer:
    """ Tracer """

    def __init__(self, wr, rs = None, tt = True):

        self.prev_tr = wr.tr # save previous tracer associated with wrapper
        wr.tr = self # associate wrapper to current tracer
        #print("new tracer")
        self.randsol = rs # assocaite random solution generator to tracer

        self.str_addr = tt
        self.reset_trace() # initialise state variables
		
    def release_wrapper(self, wr):
        wr.tr = self.prev_tr # resume previous tracer in the wrapper
        #print("released wrapper")		


    ##### TRACE METHODS

    def reset_trace(self):

        self.mode = "off"
        self.trace = OrderedDict() # {}
        self.new_trace = OrderedDict() # {}
        self.stack = []
        self.multiple = []


    def get_trace(self):

        self.reset_trace()
        self.mode = "trace" #start tracing
        output = self.randsol() #generate sample and trace
        self.mode = "off" #stop tracing

        #print(trace)
        return (output, self.trace)


    def play_trace(self, input_trace):

        self.reset_trace()
        self.mode, self.trace = "play", input_trace #set trace to input trace and play it from the beginning
        output = self.randsol() #regenerate sample corresponding to input trace if possible, or fix trace
        self.mode = "off" #stop tracing

        return (output, self.new_trace)


    ##### TRACE DISPLAY

    # FIXME: this should be part of Trace class?

    def display_trace(self, trace):

        for k in trace.keys():
            f, args, output = trace[k]
            print(k, "---->", f.__name__ + str(args) + " = " + str(output))







import inspect
from collections import defaultdict, OrderedDict, Sequence
import itertools
import os

from tracer import Tracer

class Wrapper:
    """ Wrapper """
		
    def __init__(self):
        self.tr = None ##### LINK TRACER TO WRAPPER
 
    ##### WRAPPER FUNCTIONS

    ##### TERMINALS

    def make_traceable(self, f):

        # this wrapper creates or plays and fixes the trace
        def decorated_function1(*args):

            if self.tr.mode == "off":
                return f(*args) #return output

            #terminal node: trace should not track functions called by this one
            save_mode = self.tr.mode
            self.tr.mode = "off"

            #get runtime name of current call
            addr = tuple(self.tr.stack)

            entry_type = (f,args)

            if save_mode == "trace":
                output = f(*args) #sample
                assert not addr in self.tr.trace #TRACE ADDRESS MUST BE UNIQUE
                self.tr.trace[addr] = (entry_type,output) #add to trace

            if save_mode == "play":
                if addr in self.tr.trace and entry_type == self.tr.trace[addr][0]:
                    output = self.tr.trace[addr][1] #use value from trace
                else: # if not existing or mismatch
                    output = f(*args) #sample
                self.tr.new_trace[addr] = (entry_type,output) #fixed trace

            #restore mode
            self.tr.mode = save_mode

            return output

        decorated_function1.__name__ = f.__name__
        decorated_function1.__terminal__ = True

        return decorated_function1


    ##### NON-TERMINALS

    def random_function(self, func):

        # this wrapper keeps track of the "runtime name"
        def decorated_function2(*args):

            #################
            ### no naming ###
            #################
            
            #print("*", mode, str_addr)

            if self.tr.mode == "off":
                return func(*args) #return output

            #print("r")


            #####################
            ### linear naming ###
            #####################
            
            if not self.tr.str_addr:

                #print("l")

                if hasattr(func, '__terminal__'):

                    #print("t")

                    #initialise count
                    if self.tr.stack == []:
                        self.tr.stack = [(None, None, 0)]

                    #increment count
                    count = self.tr.stack[0][2]
                    self.tr.stack = [(None, None, count+1)]

                return func(*args) #return output


            #########################
            ### structured naming ###
            #########################
            
            # 'stack' tracks recursion, 'multiple' tracks looping

            # identify function in the program by its name and its line_no in the program
            func_id = line_no, name  =  inspect.currentframe().f_back.f_lineno, func.__name__

            # get recursion level
            level = len(self.tr.stack)

            # get number of repeated call to the function in a loop
            if len(self.tr.multiple) < level+1: # it is level+1 because there can be loops at recursion level 0
                self.tr.multiple.append(defaultdict(int)) #create new "multiple" stack level

            # no need of initialisation with default dictionary
            #if not func_id in self.tr.multiple[level]:
            #    self.tr.multiple[level][func_id] = 0 #initialise top element of "multiple" stack for a new function

            #print(level, multiple, func_id)
            self.tr.multiple[level][func_id] += 1 #update top element of "multiple" stack
            mult = self.tr.multiple[level][func_id]

            # identify a specific call to a function at the current recursion level
            call_id = func_id + (mult, )

            # push call identifier on the stack
            self.tr.stack.append(call_id)
            #print(stack)

            # get the output of funct
            output = func(*args)

            # pop call identifier from the stack
            self.tr.stack.pop()
            #print(stack)

            # delete all multiple below level
            if len(self.tr.multiple) > level+1:
                self.tr.multiple.pop()
                #del self.tr.multiple[level+1] #pop "multiple" stack

            return output

        decorated_function2.__name__ = func.__name__ # need this for compare_all: but is it ok elsewhere?
        return decorated_function2

    ####

# Create wrapper object

wr = Wrapper()
Tracer(wr) ## link a new tracer to the wrapper

make_traceable = wr.make_traceable
random_function = wr.random_function

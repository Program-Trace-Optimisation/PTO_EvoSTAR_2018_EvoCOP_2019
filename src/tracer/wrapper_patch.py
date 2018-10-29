
import inspect
from collections import defaultdict, OrderedDict, Sequence
import itertools
import os

from tracer import Tracer

def compatible_type(curr_type, trace_type, trace_val):
    
    #print(curr_type, trace_type, trace_val)
    
    if curr_type == trace_type:
        return True
        
    if curr_type[0] == trace_type[0] and trace_val in curr_type[1][0]:
        print('*', end='')
        return True
        
    return False


class Wrapper:
    """ Wrapper """
		
    def __init__(self):
        self.tr = None ##### LINK TRACER TO WRAPPER

    #def fix_generator(self, rs):
    #    if not hasattr(rs, '__nonterminal__'):
    #        rs = random_function(rs)
    #    return lambda: rs()
 
    ##### WRAPPER FUNCTIONS

    ##### TERMINALS

    def make_traceable(self, f):

        # this wrapper creates or plays and fixes the trace
        def decorated_function1(*args, **kwds):

            ###############
            # Tracing OFF #
            ###############
            
            if self.tr.mode == "off":
                return f(*args, **kwds) #return output


            ##############
            # Tracing ON #
            ##############

            #terminal node: trace should not track functions called by this one
            save_mode, self.tr.mode = self.tr.mode, "off" # do we really need this?

            #get runtime name of current call
            addr = tuple(self.tr.stack)

            # get current entry type
            entry_type = (f,args) # FIXME: if using random generator with key-word args this should be (f,args,kwds)
            
            if save_mode == "trace":
                output = f(*args, **kwds) #sample
                assert not addr in self.tr.trace #TRACE ADDRESS MUST BE UNIQUE
                self.tr.trace[addr] = (entry_type,output) #add entry to trace


            ############
            # Playback #
            ############

            if save_mode == "play":
                if addr in self.tr.trace and compatible_type(entry_type, self.tr.trace[addr][0], self.tr.trace[addr][1]):
                    output = self.tr.trace[addr][1] #use value from trace
                else: # if not existing or mismatch
                    output = f(*args, **kwds) #sample
                self.tr.new_trace[addr] = (entry_type,output) #fixed trace


            #restore mode
            self.tr.mode = save_mode # do we really need this?

            return output

        decorated_function1.__name__ = f.__name__
        decorated_function1.__terminal__ = True

        return decorated_function1


    
    
    ##### NON-TERMINALS

    def random_function(self, func):

        # this wrapper keeps track of the "runtime name"
        def decorated_function2(*args, **kwds):

            #################
            ### No naming ###
            #################
            
            #print("*", mode, str_addr)

            if self.tr.mode == "off":
                return func(*args, **kwds) #return output

            #print("r")


            #####################
            ### Linear naming ###
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

                return func(*args, **kwds) #return output


            #########################
            ### Structured naming ###
            #########################

            if False: 
            
                # 'stack' tracks recursion, 'multiple' tracks looping

                # initialise multiple counts
                if self.tr.multiple == []:
                    self.tr.multiple = [defaultdict(int)]

                # identify function in the program by its name and its line_no in the program
                func_id = line_no, name  =  inspect.currentframe().f_back.f_lineno, func.__name__

                # get recursion level
                #level = len(self.tr.stack)

                # get number of repeated call to the function in a loop
                #if len(self.tr.multiple) < level+1: # it is level+1 because there can be loops at recursion level 0
                #    self.tr.multiple.append(defaultdict(int)) #create new "multiple" stack level

                # no need of initialisation with default dictionary
                #if not func_id in self.tr.multiple[level]:
                #    self.tr.multiple[level][func_id] = 0 #initialise top element of "multiple" stack for a new function

                #print(level, multiple, func_id)
                self.tr.multiple[-1][func_id] += 1 #update top element of "multiple" stack
                mult = self.tr.multiple[-1][func_id]

                # identify a specific call to a function at the current recursion level
                call_id = func_id + (mult, )

                # push multiple
                self.tr.multiple.append(defaultdict(int))

                # push call identifier on the stack
                self.tr.stack.append(call_id)
                #print(stack)

                # get the output of funct
                output = func(*args, **kwds)

                # pop call identifier from the stack
                self.tr.stack.pop()
                #print(stack)

                # pop multiple
                self.tr.multiple.pop()

                # delete all multiple below level
                #if len(self.tr.multiple) > level+1:
                #    self.tr.multiple.pop()
                    #del self.tr.multiple[level+1] #pop "multiple" stack

                return output

            ####################################
            ### Structured naming with loops ###
            ####################################

            if False: 

                # identify function in the program by:
                name = func.__name__ # function name
                line_no = inspect.currentframe().f_back.f_lineno # line number
                idx = inspect.currentframe().f_back.f_lasti      # index in code (surrogate for column number)
                loc_vars  = str({k: v for k, v in inspect.currentframe().f_back.f_locals.items() if k[0] == '_'}) # marked local vars
                call_id = func_id = name, line_no, idx, loc_vars

                # push call identifier on the stack
                self.tr.stack.append(call_id)
                #print(stack)

                # get the output of funct
                output = func(*args, **kwds)

                # pop call identifier from the stack
                self.tr.stack.pop()
                #print(stack)

                return output

            ##############################################
            ### Resilient structured naming with loops ###
            ##############################################

            else:

                # initialise multiple counts
                if self.tr.multiple == []:
                    self.tr.multiple = [defaultdict(int)]

                # identify function in the program 
                frame = inspect.currentframe().f_back 

                name = func.__name__     # function name
                line_no = frame.f_lineno # line number
                idx = frame.f_lasti      # index in code (surrogate for column number)

                # local vars    
                loc_vars = list(frame.f_locals.items())                     # local vars in the current frame
                while(frame.f_code.co_name[0] == '<'):                      # find all local vars in the calling function scope
                    #print(frame.f_code.co_name)
                    frame = frame.f_back                                    # - move to outer frame
                    loc_vars = loc_vars + list(frame.f_locals.items())      # - add local vars of outer frame

                loc_vars_str  = str({k: v for k, v in loc_vars if k[0] == '_'}) # keep the marked local vars
  
                del frame

                '''
                stack = inspect.getouterframes(inspect.currentframe(), context=1)

                name = func.__name__            # function name
                line_no = stack[0].frame.f_lineno # line number
                idx = stack[0].frame.f_lasti    # index in code (surrogate for column number)

                loc_vars = []
                for stack_entry in stack:
                    loc_vars = loc_vars + list(stack_entry.frame.f_locals.items())
                    if stack_entry.function[0] == '<': break
                loc_vars  = str({k: v for k, v in loc_vars if k[0] == '_'})

                del stack
                '''
                
                func_id = name, line_no, idx, loc_vars_str

                #print(level, multiple, func_id)
                self.tr.multiple[-1][func_id] += 1 #update top element of "multiple" stack
                mult = self.tr.multiple[-1][func_id]

                # identify a specific call to a function at the current recursion level
                call_id = func_id + (mult, )

                # push multiple
                self.tr.multiple.append(defaultdict(int))

                # push call identifier on the stack
                self.tr.stack.append(call_id)
                #print(stack)

                # get the output of funct
                output = func(*args, **kwds)

                # pop call identifier from the stack
                self.tr.stack.pop()
                #print(stack)

                # pop multiple
                self.tr.multiple.pop()

                return output

                
        decorated_function2.__name__ = func.__name__ 
        decorated_function2.__nonterminal__ = True
        return decorated_function2

    ####

# Create wrapper object

wr = Wrapper()
Tracer().acquire_wrapper(wr) ## link a new tracer to the wrapper

make_traceable = wr.make_traceable
random_function = wr.random_function




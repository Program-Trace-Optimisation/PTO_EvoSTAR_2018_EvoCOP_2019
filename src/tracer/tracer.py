from __future__ import print_function
import inspect
from collections import defaultdict, OrderedDict, Sequence
import itertools
import os

########################## TRACER ##########################

class Tracer:
    """ Tracer """

    def __init__(self):
        self.str_addr = True
        self.reset_trace() # initialise state variables

    def set_str_addr(self, str_trace):
        self.str_addr = str_trace


    ##### TRACE METHODS

    def reset_trace(self):

        self.mode = "off"
        self.trace = OrderedDict() # {}
        self.new_trace = OrderedDict() # {}
        self.stack = []
        self.multiple = []


    def get_trace(self, traceable):

        self.reset_trace()
        self.mode = "trace" #start tracing
        output = traceable() #generate sample and trace
        self.mode = "off" #stop tracing

        #print(trace)
        return (output, self.trace)


    def play_trace(self, traceable, input_trace):

        self.reset_trace()
        self.mode, self.trace = "play", input_trace #set trace to input trace and play it from the beginning
        output = traceable() #regenerate sample corresponding to input trace if possible, or fix trace
        self.mode = "off" #stop tracing

        return (output, self.new_trace)


    ##### TRACE DISPLAY

    def display_trace(self, trace):

        for k in trace.keys():
            f, args, output = trace[k]
            print(k, "---->", f.__name__ + str(args) + " = " + str(output))

    ##### WRAPPER FUNCTIONS

    ##### TERMINALS

    def make_traceable(self, f):

        # this wrapper creates or plays and fixes the trace
        def decorated_function1(*args):

            if self.mode == "off":
                return f(*args) #return output

            #terminal node: trace should not track functions called by this one
            save_mode = self.mode
            self.mode = "off"

            #get runtime name of current call
            addr = tuple(self.stack)

            if save_mode == "trace":
                output = f(*args) #sample
                assert not addr in self.trace #TRACE ADDRESS MUST BE UNIQUE
                self.trace[addr] = (f,args,output) #add to trace

            if save_mode == "play":
                if addr in self.trace and (f,args) == self.trace[addr][:2]:
                    output = self.trace[addr][2] #use value from trace
                else: # if not existing or mismatch
                    output = f(*args) #sample
                self.new_trace[addr] = (f,args,output) #fixed trace

            #restore mode
            self.mode = save_mode

            return output

        decorated_function1.__name__ = f.__name__
        decorated_function1.__terminal__ = True

        return decorated_function1


    ##### NON-TERMINALS

    def random_function(self, func):

        # this wrapper keeps track of the "runtime name"
        def decorated_function2(*args):

            #print("*", mode, str_addr)

            if self.mode == "off":
                return func(*args) #return output

            #print("r")

            ### linear naming ###

            if not self.str_addr:

                #print("l")

                if hasattr(func, '__terminal__'):

                    #print("t")

                    #initialise count
                    if self.stack == []:
                        self.stack = [(None, None, 0)]

                    #increment count
                    count = self.stack[0][2]
                    self.stack = [(None, None, count+1)]

                return func(*args) #return output


            ### structured naming ###

            # 'stack' tracks recursion, 'multiple' tracks looping

            # identify function in the program by its name and its line_no in the program
            func_id = line_no, name  =  inspect.currentframe().f_back.f_lineno, func.__name__

            # get recursion level
            level = len(self.stack)

            # get number of repeated call to the function in a loop
            if len(self.multiple) < level+1: # it is level+1 because there can be loops at recursion level 0
                self.multiple.append(defaultdict(int)) #create new "multiple" stack level

            # no need of initialisation with default dictionary
            #if not func_id in self.multiple[level]:
            #    self.multiple[level][func_id] = 0 #initialise top element of "multiple" stack for a new function

            #print(level, multiple, func_id)
            self.multiple[level][func_id] += 1 #update top element of "multiple" stack
            mult = self.multiple[level][func_id]

            # identify a specific call to a function at the current recursion level
            call_id = func_id + (mult, )

            # push call identifier on the stack
            self.stack.append(call_id)
            #print(stack)

            # get the output of funct
            output = func(*args)

            # pop call identifier from the stack
            self.stack.pop()
            #print(stack)

            # delete all multiple below level
            if len(self.multiple) > level+1:
                self.multiple.pop()
                #del self.multiple[level+1] #pop "multiple" stack

            return output

        decorated_function2.__name__ = func.__name__ # need this for compare_all: but is it ok elsewhere?
        return decorated_function2

    ####

##### DERIVATION TREE

class DerivationTree:
    # naming schemes naturally induce a tree structure (analogous to
    # the derivation tree in GE). this structure should be useful for
    # understanding the effect of search operators at a phenotype
    # level wrt a naming scheme e.g., crossover on traces can be also
    # seen as recombining aligned tree structures

    class Node:
        def __init__(self, addr_part, value=None):
            self.addr_part = addr_part
            self.value = value
            self.children = []

        def add_child(self, obj):
            self.children.append(obj)

    def __init__(self, trace):
        self.trace = trace
        self.derivation_tree = None

    def trace_to_tree(self):
        root = self.Node(())
        for address in self.trace:
            self.add_trace_entry(root, address, self.trace[address])
        self.derivation_tree = root

    def add_trace_entry(self, parent, address, value):
        addr_part = address[0] #assumes the len of adrress is >= 1

        if addr_part not in [child.addr_part for child in parent.children]:
            if len(address) == 1:
                child = self.Node(addr_part, value)
            else:
                child = self.Node(addr_part)
            parent.add_child(child)
        else:
            child = [child for child in parent.children if child.addr_part == addr_part][0]

        if len(address) > 1:
            self.add_trace_entry(child, address[1:], value)
        else:
            return

    def tree_to_trace(self):
        return self.trace # cheating as we should reconstruct trace from tree

    def sort_tree(self):
        pass

    def flatten(self, s):
        # flattens two levels of nested sequences to one level, and
        # works even if some items at the first level are not
        # sequences.
        r = []
        for item in s:
            if isinstance(item, Sequence):
                r.extend(item)
            else:
                r.append(item)
        return r

    def display_tree(self, node = None, ident = 0):

        if node == None:
            node = self.derivation_tree

        print(" " * ident, node.addr_part, " -> ",)

        if node.value is not None:
            f, args, output = node.value
            print("args", args)
            args = self.flatten(args)
            args = [ arg.__name__ if hasattr(arg, "__name__") else arg for arg in args ]
            output = output.__name__ if hasattr(output, "__name__") else output
            print(f.__name__ + str(args) + " = " + str(output))
        else:
            print(".")

        for child in node.children:
            self.display_tree(child, ident + 4)

    def tree_to_graphviz(self, filename, ext="eps"):
        """Generate a tree diagram using Graphviz."""

        # First, setup.
        ID = itertools.count(0)
        def _r(n, n_ID):
            if n.value is not None:
                f, args, output = n.value
                label = output
                if callable(label):
                    label = label.__name__
            else:
                if len(n.addr_part):
                    label = n.addr_part[1]
                else:
                    label = "generator"
            label = str(label)
            label = label.replace("&", "&amp;")
            label = label.replace("<", "&lt;")
            label = label.replace(">", "&gt;")
            label = label.replace('"', "&quot;")
            if not len(n.children):
                # it's a leaf
                # print("leaf")
                ofile.write('    n%d [label=<<B>%d</B>: %s>,style=filled,fillcolor="#DDDDDD"];\n' % (n_ID, n_ID, label))
            else:
                ofile.write('    n%d [label=<<B>%d</B>: %s>];\n' % (n_ID, n_ID, label))

            for c in n.children:
                c_ID = next(ID)
                ofile.write("    n%d -> n%d;\n" % (n_ID, c_ID))
                _r(c, c_ID)

        # Next, output to a .dot file.
        ofile = open(filename + ".dot", "w")
        ofile.write("strict digraph tree {\n")
        ofile.write("    node [shape=box];\n")
        n0 = self.derivation_tree
        _r(n0, next(ID))
        ofile.write("}\n")
        ofile.close()


        # Finally, run Graphviz. Ask it to output svg, because the
        # HTML-style font attributes only work in svg output. Then
        # convert to desired format.
        command = "dot -Tsvg -o%s.svg < %s.dot" % (filename, filename)
        command2 = "convert %s.svg %s.%s" % (filename, filename, ext)
        try:
            os.system(command)
            os.system(command2)
            print("Created %s.%s" % (filename, ext))
        except:
            print("Failed to create %s.%s. Do you have Graphviz (dot) and ImageMagick (convert)?" % (filename, ext))



#########

# Create tracer object

tr = Tracer()
make_traceable = tr.make_traceable
random_function = tr.random_function

##### WRAP ALL RANDOM FUNCTIONS (AS TERMINALS)

from random import Random

random = Random() # it creates a local random object, rather than changing the random module

for name, fn in inspect.getmembers(random, predicate=inspect.ismethod):
    if name == "shuffle": continue # handle it specially, see below
    #print(name)
    # make random functions both traceable and part of the "runtime" address
    setattr(random, name, random_function(make_traceable(fn)))
setattr(random, 'random', random_function(make_traceable(random.random)))

# Also wrap shuffle specially in order to get both in-place and return
# semantics for shuffle so user can continue to use shuffle in-place
# as usual, but tracer gets a return value in the trace (instead of
# None)
random_shuffle_saved = random.shuffle
def shuffle(x):
    random_shuffle_saved(x)
    return x
setattr(random, 'shuffle', random_function(make_traceable(shuffle)))







###################
# Test GP randsol #
###################

def test_GP_randsol_trace():

    n=3
    vars = ['x'+str(i) for i in range(n)]
    
    def GP_randsol():
        return randexpr(n)

    @random_function
    def randexpr(depth):
        'Create a random Boolean expression.'
        if depth==1 or random.uniform(0,1)<1.0/(2**depth-1):
            return random.choice(vars)
        if random.uniform(0,1)<1.0/3:
            return 'not' + ' ' + randexpr(depth-1)
        else:
            return '(' + randexpr(depth-1) + ' ' + random.choice(['and','or']) + ' ' + randexpr(depth-1) + ')'
    
    (output, trace) = tr.get_trace(GP_randsol)
    print("output:")
    print(output)
    
    print("trace:")
    print(trace)
    tr.display_trace(trace)
    
    print("trace tree:")
    dtree = DerivationTree(trace)
    dtree.trace_to_tree()
    dtree.display_tree()
    # uncomment, and it will write a file test.pdf to disk
    # dtree.tree_to_graphviz("test", "pdf")


    ############################################################


#####
if __name__ == "__main__":
    test_GP_randsol_trace()

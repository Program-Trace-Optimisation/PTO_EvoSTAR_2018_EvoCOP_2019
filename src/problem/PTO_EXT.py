# Configuration file for ipython.

# c = get_config()

############ This file should be put in  C:\Users\alberto\.ipython\profile_default

# Configuration file for ipython.

## A list of ast.NodeTransformer subclass instances, which will be applied to
#  user input before code is run.

#import sys
#sys.path.append('C:/Users/alberto/Desktop/PTO-master/src/compiler')

#from ast_annotations import ast_transformers 

######################################################################################

import ast

#=================

##### 1) IMPORT

class Import(ast.NodeTransformer):

    def visit_ImportFrom(self, node):
        if node.module == 'PTO':
            node.module = '_PTO'
            node.names = node.names + [ast.alias(name='random_function', asname=None)]
        return node


#=================

##### 2) DECORATORS

## add '@random_function' to any function definition in the file
## note: adding this decorator to the fitness function and solgen itself is harmless (i.e., does not alter their semantics)

#for node in ast.walk(tree):
#    if isinstance(node, ast.FunctionDef):
#        node.decorator_list = [ast.Name(id='random_function', ctx=ast.Load())] + node.decorator_list

class RandFuncDec(ast.NodeTransformer):
    """ Add @random_function to any function definition """
    
    def visit_FunctionDef(self, node):
        node.decorator_list = [ast.Name(id='random_function', ctx=ast.Load())] + node.decorator_list
        return node


#=================

##### 3) COMPREHENSIONS

## add an initial underscore to loop variables in various types of comprehensions (list, set, dict, generator)
## this is done to any comprehension in the file
## note: as loop variables of comprehensions are local variables to the comprehensions, this transformation does not alter their semantics

#for node in ast.walk(tree):
#    if isinstance(node, ast.ListComp) or isinstance(node, ast.SetComp) or isinstance(node, ast.GeneratorExp) or isinstance(node, ast.DictComp):
#        var_names = [comp.target.id for comp in node.generators]
#        for sub_node in ast.walk(node):
#            if isinstance(sub_node, ast.Name):
#                if sub_node.id in var_names:
#                    sub_node.id = '_' + sub_node.id

class CompVar(ast.NodeTransformer):
    """ Add an initial underscore to loop variables in various types of comprehensions (list, set, dict, generator) """

    def visit_ListComp(self, node):
        var_names = [comp.target.id for comp in node.generators]
        for sub_node in ast.walk(node):
            if isinstance(sub_node, ast.Name):
                if sub_node.id in var_names:
                    sub_node.id = '_' + sub_node.id
        return node

    def visit_SetComp(self, node):
        var_names = [comp.target.id for comp in node.generators]
        for sub_node in ast.walk(node):
            if isinstance(sub_node, ast.Name):
                if sub_node.id in var_names:
                    sub_node.id = '_' + sub_node.id
        return node

    def visit_GeneratorExp(self, node):
        var_names = [comp.target.id for comp in node.generators]
        for sub_node in ast.walk(node):
            if isinstance(sub_node, ast.Name):
                if sub_node.id in var_names:
                    sub_node.id = '_' + sub_node.id
        return node
        
    def visit_DictComp(self, node):
        var_names = [comp.target.id for comp in node.generators]
        for sub_node in ast.walk(node):
            if isinstance(sub_node, ast.Name):
                if sub_node.id in var_names:
                    sub_node.id = '_' + sub_node.id
        return node


#=================

##### 4) FOR LOOPS

## add an initial underscore to all for loop variables including nested loops
## note: to preserve the semantics, as loops are not locally scoped, all occurences of loop variables in the enclosing local scope of the loop should be modified 

#for node in ast.walk(tree):
#    if isinstance(node, ast.FunctionDef):
#        for sub_node in ast.walk(node):
#            if isinstance(sub_node, ast.For):
#                var_name = sub_node.target.id
#                for sub_node in ast.walk(node):
#                    if isinstance(sub_node, ast.Name):
#                        if sub_node.id == var_name:
#                            sub_node.id = '_' + sub_node.id

class LoopVar(ast.NodeTransformer):
    """ Add an initial underscore to all for loop variables including nested loops """
    
    def visit_FunctionDef(self, node):
        for sub_node in ast.walk(node):
            if isinstance(sub_node, ast.For):
                var_name = sub_node.target.id
                for sub_node in ast.walk(node):
                    if isinstance(sub_node, ast.Name):
                        if sub_node.id == var_name:
                            sub_node.id = '_' + sub_node.id
        return node


                
#=================

##### 5) WHILE LOOPS

## add a counter variable starting with an underscore to all (non-nested) while loops in all functions
## the counter must be initialised before the while loop, and incremented inside the while loop
## note: this addition does not alter the semantics, as long as the name of the counter does not clash with any other variable name
## note: adding counters to nested while loop yet to be implemented

#for node in ast.walk(tree):
#    if isinstance(node, ast.FunctionDef):
#        new_body = []
#        for i in range(len(node.body)):
#            #print i, len(node.body)
#            if isinstance(node.body[i], ast.While):
#                while_node = node.body[i]
#                init_node = ast.Assign(targets=[ast.Name(id='_i', ctx=ast.Store())], value=ast.Num(n=0))
#                while_node.body = [ast.AugAssign(target=ast.Name(id='_i', ctx=ast.Store()), op=ast.Add(), value=ast.Num(n=1))] + while_node.body
#                new_body += [init_node, while_node]
#            else:
#                new_body += [node.body[i]]
#        node.body = new_body

class WhileVar(ast.NodeTransformer):
    """ Add counters to all non-nested while loops """

    def visit_FunctionDef(self, node):
        new_body = []
        for i in range(len(node.body)):
            #print i, len(node.body)
            if isinstance(node.body[i], ast.While):
                while_node = node.body[i]
                init_node = ast.Assign(targets=[ast.Name(id='_i', ctx=ast.Store())], value=ast.Num(n=0))
                while_node.body = [ast.AugAssign(target=ast.Name(id='_i', ctx=ast.Store()), op=ast.Add(), value=ast.Num(n=1))] + while_node.body
                new_body += [init_node, while_node]
            else:
                new_body += [node.body[i]]
        node.body = new_body
        return node


#=================

##### LIST OF TRANFORMERS

ast_transformers = [Import(), RandFuncDec(), CompVar(), LoopVar(), WhileVar()]


######################################################################################

def load_ipython_extension(ipython):
    """This function is called when the extension is
    loaded. It accepts an IPython InteractiveShell
    instance. We can register the magic with the
    `register_magic_function` method of the shell
    instance."""
	ipython.exec_lines = ['from _PTO import random_function']
    ipython.ast_transformers = ast_transformers


# c.InteractiveShell.ast_transformers = ast_transformers

######################################################################################

# executes the line in brackets on program launch
# c.InteractiveShellApp.exec_lines = ['from _PTO import random_function']
 

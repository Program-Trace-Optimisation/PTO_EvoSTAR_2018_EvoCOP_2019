import ast
import astor.code_gen
#import astpp
#import sys

from ast_annotations import ast_transformers 

## USAGE:

## read program name form command line e.g., compile ga.py
## produce in output a compiled version of the program e.g., #_ga.py
## you can open _ga.py in idle and run it

def annotate(file_name):

    ##### INPUT

    ## the input program should be read in the variable prog

    #file_name = sys.argv[1]

    with open(file_name, 'r') as myfile:
      prog = myfile.read()


    ##### parse the program into a tree #

    tree = ast.parse(prog)

    ##### apply transformations

    for t in ast_transformers:
      tree = t.visit(tree)

    ##### covert the tree back to a program

    prog = astor.code_gen.to_source(tree)

    ##### OUTPUT

    ## the output program should be written to a file

    file_name = '_'+file_name

    with open(file_name, "w") as text_file:
        text_file.write(prog)


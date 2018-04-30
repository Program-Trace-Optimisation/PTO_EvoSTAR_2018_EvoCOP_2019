
############ This file should be put in  C:\Users\alberto\.ipython\profile_default

# Configuration file for ipython.

## A list of ast.NodeTransformer subclass instances, which will be applied to
#  user input before code is run.

import sys
sys.path.append('C:/Users/alberto/Desktop/PTO-master/src/compiler')

from ast_annotations import ast_transformers 

c.InteractiveShell.ast_transformers = ast_transformers 


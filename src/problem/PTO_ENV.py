
### CODE PREPROCESSING ###

### GET IMPORTING MODULE NAME

from inspect import getframeinfo, getouterframes, currentframe, getmodulename
frame = currentframe().f_back
while frame.f_code.co_filename.startswith('<frozen'):
    frame = frame.f_back
calling_module = getmodulename(frame.f_code.co_filename)

print(calling_module)

import sys
sys.path.append('../compiler')

if frame.f_code.co_filename.startswith('<ipython'): 
    # this is triggered by "import PTO_ENV" from ipython (notebook mode)

    from ast_annotations import ast_transformers
    ipython=get_ipython()
    ipython.ex('from PTO import random_function')
    ipython.ast_transformers = ast_transformers
    
elif calling_module == '__init__':
    # this is triggered by "load_ext PTO_ENV" from ipython (notebook mode as extension)
    
    def load_ipython_extension(ipython):
        """This function is called when the extension is
        loaded. It accepts an IPython InteractiveShell
        instance. We can register the magic with the
        `register_magic_function` method of the shell
        instance."""
        from ast_annotations import ast_transformers
        ipython.ex('from PTO import random_function')
        ipython.ast_transformers = ast_transformers
    
else: # this is triggered by "import PTO_ENV" from file (batch mode)

    ### ANNOTATE CODE

    from compile import annotate

    annotate(calling_module+".py")       

    ### RUN ANNOTATED CODE

    __import__('_'+calling_module)

    ### BYPASS ORIGINAL CODE

    sys.exit() 


####################################################################################


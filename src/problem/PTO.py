
### CODE PREPROCESSING ###

### GET IMPORTING MODULE NAME

import sys

sys.path.append('../compiler')

from inspect import getframeinfo, getouterframes, currentframe, getmodulename
frame = currentframe().f_back
while frame.f_code.co_filename.startswith('<frozen'):
    frame = frame.f_back
calling_module = getmodulename(frame.f_code.co_filename)

#print(calling_module)

### ANNOTATE CODE

from compile import annotate

annotate(calling_module+".py")       

### RUN ANNOTATED CODE

__import__('_'+calling_module)

### BYPASS ORIGINAL CODE

sys.exit() 



###### DETERMINE AVERAGE SIZE FOR PARAMETER SETTING

AVG_SIZE = {} # memoise avg size in a class variable to prevent recomputation in different solve calls
def avg_size_trace(tr):
    
    if not tr.randsol in AVG_SIZE:

        #print("computing avg size", end="")
        curr_cum_size, curr_iter = sum([len(tr.get_trace()[1]) for _ in range(1000)]), 1000
        curr_avg_size = 1.0 * curr_cum_size / curr_iter
        prev_avg_size = 0
        while abs(1-prev_avg_size/curr_avg_size) > 0.001: # coverged within 1% tolerance?
            #print(".", end="")
            prev_avg_size = curr_avg_size
            curr_cum_size += sum([len(tr.get_trace()[1]) for _ in range(1000)])
            curr_iter += 1000
            curr_avg_size = 1.0 * curr_cum_size / curr_iter
        
        AVG_SIZE[tr.randsol] = int(curr_avg_size)
        #print(" average trace size: ", int(curr_avg_size))
        
    return AVG_SIZE[tr.randsol]

######

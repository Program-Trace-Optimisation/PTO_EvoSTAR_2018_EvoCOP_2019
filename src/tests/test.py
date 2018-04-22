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

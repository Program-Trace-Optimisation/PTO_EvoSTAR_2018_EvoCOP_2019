#!/usr/bin/env python

import numpy as np

"""Late-acceptance hill-climbing as proposed in
http://www.yuribykov.com/LAHC/LAHC-TR.pdf

A simple modification to the basic hill-climbing algorithm. We accept
a move to a point if the point is as good as the point we encountered
h steps ago. It helps escape some local optima. However, it seems to
be worse than HC (and others) on easy problems and when the number of
iterations available is small.

Not to be confused with an acceptance to the GECCO late-breaking
papers track.

"""


######################### HILL CLIMBER #########################

class LA:
    """ Late Acceptance Hill Climbing Class """

    """The following is the pseudo-code provided by the authors. It
translates fairly directly to the code below. In PTO we maximise, so
all the <= become >=.

Produce an initial solution s
Calculate initial cost function C(s)
Specify Lfa,
For all k in {0...L_fa-1} f_k := C(s)
First iteration I=0;
Do until a chosen stopping condition
    Construct a candidate solution s*
    Calculate its cost function C(s*)
    v := I mod L_fa
    If C(s*)<=f_v or C(s*)<=C(s)
    Then accept the candidate (s:=s*)
    Else reject the candidate (s:=s)
    Insert the current cost into the fitness array f_v:=C(s)
    Increment the iteration number I:=I+1

    """

    def __init__(self, ops, budget, LFA=None):
        self.ops = ops

	self.NUMBER_GENERATION = budget
        self.data = []
        self.LFA = LFA

        if LFA is None:
            # FIXME read more papers for a better heuristic choice here
            self.LFA = max(10, self.NUMBER_GENERATION / 1000)
            self.LFA = min(self.LFA, self.NUMBER_GENERATION / 2)
        assert self.LFA <= self.NUMBER_GENERATION
        print(self.LFA)

    def run(self):

        s = self.ops.create_ind()
        Cs = self.ops.evaluate_ind(s)
        self.data = [Cs]
        best = s
        Cbest = Cs
        f = Cs * np.ones(self.LFA) # If LFA is large, an array will be more efficient than a list
        for I in range(self.NUMBER_GENERATION):
            s_ = self.ops.mutate_ind(s)
            Cs_ = self.ops.evaluate_ind(s_)
            if Cs_ >= Cbest:
                Cbest = Cs_
                best = s_
            v = I % self.LFA
            if Cs_ >= f[v] or Cs_ >= Cs:
                s = s_
                Cs = Cs_
            f[v] = Cs
            self.data.append(Cbest)
        return best, Cbest

#################################################################


import random, copy

from REP_FACTORY import REP_factory
from REP import REP

    ##### POLYMORPHIC REPRESENTATION #####

class POLY_REP:
    """ Determine the representation to use for the entry """

    def __init__(self, fine_ops):
        
        self.fine_ops = fine_ops

    def perturb(self, entry):

        typ = entry[0]
        rep = REP() if not self.fine_ops else REP_factory(typ) # if no fine operators required use generic representation
        if not rep: rep = REP()                                # if no fine operators available use generic representation
        return rep.perturb(entry)

    def blend(self, entry1, entry2):

        typ1, typ2 = entry1[0], entry2[0]
        if typ1 != typ2:   # if incompatible parents  
            rep = REP()    # use generic representation
        else:
            rep = REP() if not self.fine_ops else REP_factory(typ1)
            if not rep: rep = REP()
        return rep.blend(entry1, entry2)

    def combine(self, entry_pool):

        typ1 = entry_pool[0][0]
        if [typ for (typ, _) in entry_pool].count(typ1) < len(entry_pool): # if not all compatible
            rep = REP()                                                    # use generic representation  
        else:
            rep = REP() if not self.fine_ops else REP_factory(typ1)
            if not rep: rep = REP()
        return rep.combine(entry_pool)
        


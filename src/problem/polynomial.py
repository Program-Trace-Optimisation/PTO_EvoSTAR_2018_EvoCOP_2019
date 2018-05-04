import itertools
import random
import numpy as np

class Polynomial:
    def __init__(self, degree, nvars, coefs):
        self.degree = degree
        self.nvars = nvars
        self.coefs = coefs

    @staticmethod
    def terms(degree, nvars):
        for pows in itertools.product(range(degree + 1), repeat=nvars):
            if sum(pows) <= degree:
                yield pows

    @classmethod
    def from_random(cls, degree, nvars):
        coefs = [2*(random.random() - 0.5) for i in Polynomial.terms(degree, nvars)]
        p = Polynomial(degree, nvars, coefs)
        return p

    def __str__(self):
        def s(pows):
            if sum(pows):
                return "*" + "*".join("x[%d]**%d" % (i, powi)
                                      for i, powi in enumerate(pows) if powi > 0)
            else:
                return "" # this term is a const so the coef on its own is enough
        return " + ".join("%.3f%s" % (coef, s(pows))
                          for (coef, pows) in
                          zip(self.coefs, Polynomial.terms(self.degree, self.nvars)))

    def eval(self, x):
        assert x.shape[0] == self.nvars
        result = np.zeros(x.shape[1]) # same length as a column of x
        for coef, pows in zip(self.coefs, self.terms(self.degree, self.nvars)):
            tmp = np.ones(x.shape[1])
            for (xi, pow) in zip(x, pows):
                tmp *= (xi ** pow)
            tmp *= coef
            result += tmp
        return result

if __name__ == "__main__":
    # deg = 3
    # nvars = 1
    # nrows = 10
    # coefs = [1, 1, 2, 1]
    # x = np.random.random((nvars, nrows))

    # # print(Polynomial(6, 1))
    # # print(Polynomial(6, 3))
    # p = Polynomial(deg, nvars, coefs)
    # print(p)
    # print(p.eval(x))

    deg = 2
    nvars = 2
    nrows = 10
    #x = np.random.random((nvars, nrows))
    x = np.ones((nvars, nrows))
    p = Polynomial.from_random(deg, nvars)
    print(p)
    print(x.T)
    print(p.eval(x))

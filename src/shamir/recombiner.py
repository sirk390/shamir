import random
import operator
from shamir.polynomial import LagrangePolynomial

class SecretRecombiner():
    def __init__(self, field):
        self.field = field
   
    def recombine(self, shares, x_recomb):
        xs, ys = zip(*shares)
        p = LagrangePolynomial(shares, self.field.zero(), self.field.one())
        return p.evaluate(x_recomb)

    def recombine_polynomial(self, shares):
        xs, ys = zip(*shares)
        p = LagrangePolynomial(shares, self.field.zero(), self.field.one())
        return p.get_polynomial()

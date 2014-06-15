import random
import operator

class SecretRecombiner():
    def __init__(self, field):
        self.field = field
   
    def recombine(self, shares, x_recomb):
        xs, ys = zip(*shares)

        vector = []
        for i, x_i in enumerate(xs):
            factors = [((x_k - x_recomb) / (x_k - x_i))
                       for k, x_k in enumerate(xs) if k != i]
            vector.append(reduce(operator.mul, factors))
        return sum(map(operator.mul, ys, vector), self.field.zero())

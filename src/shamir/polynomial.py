import operator
import itertools

class Polynomial(object):
    def __init__(self, coefs, zero=0):
        """ coefs: Heighest degree first """
        self.coefs = coefs or [zero]
        self.zero = zero
   
    def degree(self):
        return len(self.coefs)-1
    
    def evaluate(self, x):
        """ Evaluate at x using Horner's method """
        val = self.coefs[0]
        for c in self.coefs[1:]:
            val = val*x + c
        return val

    def iter_degree_coefs(self):
        d = self.degree()
        for i, c in enumerate(self.coefs):
            yield d - i
            
    def __eq__(self, other):
        return self.coefs == other.coefs

    def __add__(self, other):
        assert type(other) is Polynomial
        res_coefs = [self.zero] * max(len(self.coefs), len( other.coefs))
        for i in range(0,len(self.coefs)):
            res_coefs[i+len(res_coefs)-len(self.coefs)] = self.coefs[i]
        for i in range(0,len(other.coefs)):
            res_coefs[i+len(res_coefs)-len(other.coefs)] += other.coefs[i]
        return Polynomial(res_coefs, self.zero)

    def __mul__(self, other):
        if type(other) is Polynomial:
            res_coefs = [self.zero] * (len(self.coefs)+len(other.coefs)-1)
            for j in range(0, len(self.coefs)):
                for i in range(0, len(other.coefs)):
                    res_coefs[(i+j)] += self.coefs[j] * other.coefs[i]
            return Polynomial(res_coefs, self.zero)
        else:
            return Polynomial([c * other for c in self.coefs], self.zero)

    def __div__(self, other):
        if type(other) is Polynomial:
            raise NotImplemented()
        else:
            return Polynomial([c / other for c in self.coefs], self.zero)
        
    @classmethod
    def from_roots(cls, roots):
        """ Create a polynomial from the roots [r1, r2, r3 ... ] :
            (x - r1)(x - r2)(x - r3) ... """
        polys = [Polynomial([1, -r]) for r in roots]
        return reduce(operator.mul, polys)
        
    def __repr__(self):
        # not supported 
        # 1/ 0 values  Polynomial:0.333333333333x^2+0.0x+-0.333333333333
        def repr_variable(degree):
            if degree == 0:
                return ""
            elif degree == 1:
                return "x"
            else:
                return  "x^" + str(degree)
        d = self.degree()            
        strs = [(str(c) + repr_variable(d-i)) for i, c in enumerate(self.coefs)]
        return "<Polynomial:%s>" % ("+".join(strs))
    
class PointSet(object):
    def __init__(self, points, zero=0, one=1):
        self.points = points
        self.zero = zero
        self.one = one
        
    def iter_ys(self):
        for _x, y in self.points:
            yield y

    def iter_xs(self):
        for x, _y in self.points:
            yield x
            
    def evaluate_lagrange(self, x):
        """ Evaluation without computing the polynomial """
        vector = []
        for j, (x_j, y_j) in enumerate(self.points):
            factors = [((x - x_i) / (x_j - x_i))
                       for i, (x_i, y_i) in enumerate(self.points) if i != j]
            vector.append(reduce(operator.mul, factors))
        return sum(map(operator.mul, self.iter_ys(), vector), self.zero)
    

    def get_lagrange_multiplier_polynomials(self):
        multiplier_polynoms = []
        for j, (x_j, y_j) in enumerate(self.points):
            pols = []
            for i, x_i in enumerate(self.iter_xs()):
                if i != j:
                    pols.append(Polynomial([self.one, -x_i], self.zero) / (x_j - x_i))
            multiplier_polynoms.append(reduce(operator.mul, pols))
        return multiplier_polynoms
    
    def get_lagrange_polynomial(self):
        polys = []
        for p, y in zip( self.get_lagrange_multiplier_polynomials(), self.iter_ys()):
            polys.append(p * y)
        return reduce(operator.add, polys)


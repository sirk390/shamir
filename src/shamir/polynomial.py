
class Polynomial(object):
    def __init__(self, coefs):
        """ coefs: Heighest degree first """
        self.coefs = coefs
   
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
        
    def __repr__(self):
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
    

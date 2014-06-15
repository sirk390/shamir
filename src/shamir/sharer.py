from shamir.polynomial import Polynomial

class SecretSharer():
    def __init__(self, field, random):
        self.field = field
        self.random = random
   
    def share(self, secret, threshold, points):
        coef = [secret]
        coef += [self.random.randitem() for j in range(threshold)]
        p = Polynomial(list(reversed(coef)))
        shares = [(pt, p.evaluate(pt)) for pt in points]
        return shares

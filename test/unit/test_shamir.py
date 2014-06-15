import unittest
import itertools
from shamir.sharer import SecretSharer
from shamir.recombiner import SecretRecombiner
from shamir.field import ZpField
from shamir.polynomial import Polynomial

class FixedSequenceRandom():
    def __init__(self, seq):
        self.seq = seq
        self.iter = iter(seq)
        
    def randitem(self):
        return next(self.iter)


class TestShamir(unittest.TestCase):
    def test_shamir_share(self):
        field = ZpField(37)
        V = field.value_type
        numshares = 7
        sharer = SecretSharer(field,  
                              FixedSequenceRandom([V(4), V(21), V(33)])) # 3 numbers are required for threshold=3
        shares = sharer.share(V(12), 3, [V(i+1) for i in range(numshares)])
        self.assertEquals(shares,
                          [(V(1), V(33)), 
                           (V(2), V(35)), 
                           (V(3), V(31)), 
                           (V(4), V(34)), 
                           (V(5), V(20)), 
                           (V(6), V(2)), 
                           (V(7), V(30))])
        
    def test_shamir_recombine_threshold3_shares4(self):
        field = ZpField(37)
        V = field.value_type
        recombiner = SecretRecombiner(field)
        #4 shares OK: secret is recovered
        secret = recombiner.recombine([(V(2), V(35)), 
                                   (V(7), V(30)),
                                   (V(5), V(20)), 
                                   (V(4), V(34))], x_recomb=V(0))
        self.assertEquals(secret,
                          V(12))

    def test_shamir_recombine_threshold3_shares4_polynomial(self):
        field = ZpField(37)
        V = field.value_type
        recombiner = SecretRecombiner(field)
        #4 shares OK: secret is recovered
        polynom = recombiner.recombine_polynomial([(V(2), V(35)), 
                                                   (V(7), V(30)),
                                                   (V(5), V(20)), 
                                                   (V(4), V(34))])
        self.assertEquals(polynom, Polynomial([V(33), V(21), V(4), V(12)]))
        

    def test_shamir_recombine_threshold3_shares5(self):
        field = ZpField(37)
        V = field.value_type
        recombiner = SecretRecombiner(field)
        #5 shares OK: secret is recovered
        secret = recombiner.recombine([(V(6), V(2)), 
                                   (V(2), V(35)),
                                   (V(4), V(34)), 
                                   (V(7), V(30)), 
                                   (V(5), V(20))], x_recomb=V(0))

    def test_shamir_recombine_threshold3_shares6(self):
        field = ZpField(37)
        V = field.value_type
        recombiner = SecretRecombiner(field)
        #5 shares OK: secret is recovered
        secret = recombiner.recombine([(V(6), V(2)), 
                                   (V(2), V(35)),
                                   (V(3), V(31)), 
                                   (V(4), V(34)), 
                                   (V(7), V(30)), 
                                   (V(5), V(20))], x_recomb=V(0))
        self.assertEquals(secret,
                          V(12))
    def test_shamir_recombine_threshold3_shares3(self):
        field = ZpField(37)
        V = field.value_type
        recombiner = SecretRecombiner(field)
        #3 shares NOK: random result
        secret = recombiner.recombine([(V(2), V(35)),
                                   (V(4), V(34)), 
                                   (V(5), V(20))], x_recomb=V(0))
        self.assertEquals(secret,
                          V(0))

if __name__ == "__main__":
    unittest.main()
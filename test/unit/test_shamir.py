import unittest
import itertools
from shamir.shamir import ShamirPointSharer, ShamirSharer
from shamir.field import ZpField
from shamir.polynomial import Polynomial
from shamir.random_source import UnitTestRandomSource


class TestShamir(unittest.TestCase):
    def test_shamir_share(self):
        field = ZpField(37, UnitTestRandomSource([4, 21, 33]))
        V = field.value_type
        numshares = 7
        sharer = ShamirPointSharer(field) # 3 numbers are required for threshold=3
        shares = sharer.share(V(12), 3, [V(i+1) for i in range(numshares)])
        self.assertEquals(shares,
                          [(V(1), V(0)), 
                           (V(2), V(30)), 
                           (V(3), V(28)), 
                           (V(4), V(31)), 
                           (V(5), V(2)), 
                           (V(6), V(15)), 
                           (V(7), V(33))])
        
    def test_shamir_recombine_threshold3_shares4(self):
        field = ZpField(37)
        V = field.value_type
        recombiner = ShamirPointSharer(field)
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
        recombiner = ShamirPointSharer(field)
        #4 shares OK: secret is recovered
        polynom = recombiner.recombine_polynomial([(V(2), V(35)), 
                                                   (V(7), V(30)),
                                                   (V(5), V(20)), 
                                                   (V(4), V(34))])
        self.assertEquals(polynom, Polynomial([V(33), V(21), V(4), V(12)]))
        

    def test_shamir_recombine_threshold3_shares5(self):
        field = ZpField(37)
        V = field.value_type
        recombiner = ShamirPointSharer(field)
        #5 shares OK: secret is recovered
        secret = recombiner.recombine([(V(6), V(2)), 
                                   (V(2), V(35)),
                                   (V(4), V(34)), 
                                   (V(7), V(30)), 
                                   (V(5), V(20))], x_recomb=V(0))

    def test_shamir_recombine_threshold3_shares6(self):
        field = ZpField(37)
        V = field.value_type
        recombiner = ShamirPointSharer(field)
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
        recombiner = ShamirPointSharer(field)
        #3 shares NOK: random result
        secret = recombiner.recombine([(V(2), V(35)),
                                   (V(4), V(34)), 
                                   (V(5), V(20))], x_recomb=V(0))
        self.assertEquals(secret,
                          V(0))

    def test_shamir_share_string(self):
        pass
    def test_shamir_recombine_string(self):
        shamir = ShamirSharer()
        
        data = ["0090b9e7ef2119bf791ce62df82068be278cc98338a341199de3a3c9c85a6d650882358ef3f98b686e7ca881",
                "010572f3f16c6dd2bef170f26dd8f02936758cf5d7b037d7b893cc0123586afe80bd6b5a59356e94a601bfda",
                "02d59489265170a231e8c0afd3950db14d21b9cdfc9157a5c1849b19895f69eadb180685a01723fdc8f5b471"]
    
        result =  shamir.recombine([i.decode("hex") for i in data])
        
        self.assertEquals(result, "the quick brown fox jumps over the lazy dog")


if __name__ == "__main__":
    unittest.main()

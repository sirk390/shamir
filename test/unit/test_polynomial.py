import unittest
import itertools
from shamir.sharer import SecretSharer
from shamir.recombiner import SecretRecombiner
from shamir.field import ZpField
from shamir.polynomial import Polynomial


class TestPolynomial(unittest.TestCase):
    def test_Polynomial_repr(self):
        p = Polynomial([3, 5, 78, 2])
        
        self.assertEquals(repr(p), "<Polynomial:3x^3+5x^2+78x+2>")

    def test_Polynomial_evaluate_ValueIsCorrect(self):
        p = Polynomial([3, 5, 78, 2])
        
        value = p.evaluate(3)
        
        self.assertEquals(value, 362)
   
   
if __name__ == "__main__":
    unittest.main()
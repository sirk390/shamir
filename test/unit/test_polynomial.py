import unittest
import itertools
from shamir.shamir import Shamir
from shamir.field import ZpField
from shamir.polynomial import Polynomial, PointSet


class TestPolynomial(unittest.TestCase):
    def test_Polynomial_repr(self):
        p = Polynomial([3, 5, 78, 2])
        
        self.assertEquals(repr(p), "<Polynomial:3x^3+5x^2+78x+2>")

    def test_Polynomial_evaluate_ValueIsCorrect(self):
        p = Polynomial([3, 5, 78, 2])
        
        value = p.evaluate(3)
        
        self.assertEquals(value, 362)
   
    def test_Polynomial_mult(self):
        
        self.assertEquals(Polynomial([3, 5]) * Polynomial([2]), Polynomial([6, 10]))
        self.assertEquals(Polynomial([3, 5]) * Polynomial([4, 5]), Polynomial([12, 35, 25]))

    def test_Polynomial_add(self):
        self.assertEquals(Polynomial([3, 5, 9]) + Polynomial([4, 5]), 
                          Polynomial([3, 9, 14]))


    def test_Polynomial_multByInteger(self):
        self.assertEquals(Polynomial([3, 5]) * 2, Polynomial([6, 10]))
        self.assertEquals(Polynomial([3, 5]) * 6, Polynomial([18, 30]))
   
    def test_Polynomial_from_factored_form(self):
        p = Polynomial.from_roots([4, 7, 9])
        self.assertEquals(p, Polynomial([1, -20, 127, -252]))
    
class TestLagrangePolynomial(unittest.TestCase):
    def test_1(self):
        p = PointSet([(1.0, 3.0), (-1.0, 2.0), (2.0, -1.0)]).get_lagrange_polynomial()
        self.assertEquals( p, Polynomial([-1.5, 0.5, 4.0]))
        
if __name__ == "__main__":
    unittest.main()
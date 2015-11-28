from shamir.extended_gcd import extended_gcd
import unittest


class TestGCD(unittest.TestCase):
    def test_extended_gcd(self):
        n1, n2 = 252,105
        
        a, b, gcd = extended_gcd(n1, n2)
        self.assertEquals(gcd, 21)
        self.assertEquals(a, -2)
        self.assertEquals(b, 5)
        self.assertEquals(a*n1+b*n2, gcd) # bezout's identify: just for documentation


if __name__ == "__main__":
    unittest.main()

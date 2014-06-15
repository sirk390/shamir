def extended_gcd(n1, n2):
    """Return (bezout_a, bezout_b, gcd) using the extended euclidean algorithm."""
    x, lastx = 0, 1
    y, lasty = 1, 0
    while n2 != 0:
        quotient = n1 // n2
        n1, n2 = n2, n1 % n2
        x, lastx = lastx - quotient*x, x
        y, lasty = lasty - quotient*y, y
    bezout_a = lastx
    bezout_b = lasty
    gcd = n1
    return (bezout_a, bezout_b, gcd)


if __name__ == "__main__":
    import unittest
    
    class TestGCD(unittest.TestCase):
        def test_extended_gcd(self):
            n1, n2 = 252,105
            
            a, b, gcd = extended_gcd(n1, n2)
            self.assertEquals(gcd, 21)
            self.assertEquals(a, -2)
            self.assertEquals(b, 5)
            self.assertEquals(a*n1+b*n2, gcd) # bezout's identify: just for documentation
            
    unittest.main()
    
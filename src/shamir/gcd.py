
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
    
            
    unittest.main()
    
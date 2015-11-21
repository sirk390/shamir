import random
from gcd import extended_gcd
from random_source import SecureRandomSource

def make_zp_value_type(modulus):
    class ZpValue(object):
        def __init__(self, value):
            assert (0 <= value < modulus)
            self.value = value
        def __neg__(self):
            return ZpValue((-self.value) % modulus)
        def __add__(self, other):
            return ZpValue((self.value + other.value) % modulus)
        def __cmp__(self, other):
            return cmp(self.value, other.value)
        def __eq__(self, other):
            return self.value == other.value
        def __hash__(self):
            return hash(self.value)
        def __sub__(self, other):
            return ZpValue((self.value - other.value) % modulus)
        def __mul__(self, other):
            return ZpValue((self.value * other.value) % modulus)
        def __pow__(self, other):
            return ZpValue(pow(self.value, other.value, modulus))
        def __str__(self):
            return str(self.value)
        def __repr__(self):
            return repr(self.value)
        def __invert__(self):
            if self.value == 0:
                raise ZeroDivisionError()
            bezout_a, _, _ = extended_gcd(self.value, modulus)
            return ZpValue(bezout_a % modulus)
        def __div__(self, other):
            return self * ~other
        def __int__(self):
            return self.value
    return ZpValue
    
class ZpField(object):
    """ZpZ field with the given modulus"""
    def __init__(self, modulus=257, random_source=SecureRandomSource()):
        self.modulus = modulus
        self.value_type = make_zp_value_type(self.modulus)
        self.random_source = random_source
    def zero(self):
        return self.value_type(0)
    def one(self):
        return self.value_type(1)
    def random(self):
        return self.value_type(self.random_source.randrange(0, self.modulus))

if __name__ == "__main__":
    field = ZpField(37)
    Z = field.value_type
    a = Z(12)
    print sum([Z(11), Z(23)], field.zero())

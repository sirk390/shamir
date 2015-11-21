from polynomial import Polynomial, PointSet
from field import ZpField
from utils import iterslices, joinbase, splitbase
from struct import pack, unpack
from random_source import SecureRandomSource

class ShamirPointSharer(object):
    def __init__(self, field):
        self.field = field
   
    def share(self, secret, threshold, points):
        coef = [secret]
        coef += [self.field.random() for j in range(threshold-1)]
        p = Polynomial(list(reversed(coef)))
        shares = [(pt, p.evaluate(pt)) for pt in points]
        return shares

    def recombine(self, shares, x_recomb):
        p = PointSet(shares, self.field.zero(), self.field.one())
        return p.evaluate_lagrange(x_recomb)

    def recombine_polynomial(self, shares):
        p = PointSet(shares, self.field.zero(), self.field.one())
        return p.get_lagrange_polynomial()


def encode_share(share_idx, values):
    """ values are values from 0 to 256 (just more than 1 byte) """
    res = pack('B', share_idx)
    for b in values:
        if b == 0 or b == 256:
            res += "\x00" + chr(0 if b == 0 else 1)
        else:
            res += chr(b)
    return res

def decode_share(share):
    """ values are values from 0 to 256 (just more than 1 byte) """
    share_idx, = unpack('B', share[:1])
    values = []
    escape = False
    for c in share[1:]:
        if c == "\x00" and not escape:
            escape = True
        else:
            if escape:
                values.append(0 if ord(c) == 0 else 256)
                escape = False
            else:
                values.append(ord(c))
    return share_idx, values

class ShamirSharer(object):
    def __init__(self, random_source=SecureRandomSource()):
        self.field = ZpField(257, random_source=random_source)
        self.V = self.field.value_type
        self.sharer = ShamirPointSharer(self.field)
        
    def share(self, secret_string, threshold, numshares):
        all_shares = []
        for c in secret_string:
            shares = self.sharer.share(self.V(ord(c)), threshold, [self.V(i+1) for i in range(numshares)])
            share_values = [value for idx, value in shares]
            all_shares.append(share_values)
        return [encode_share(idx, [s.value for s in shares]) for idx, shares in enumerate(zip(*all_shares))]
        
    def recombine(self, shares):
        decoded_shares = [decode_share(s) for s in shares]
        share_zp_indexes = [self.V(share_idx+1) for share_idx, values in decoded_shares]
        decoded_zp_shares = zip(*[[self.V(v) for v in values] for share_idx, values in decoded_shares])
        result = ""
        for shares in decoded_zp_shares:
            result += chr(self.sharer.recombine(zip(share_zp_indexes, shares), self.V(0)))
        return result
        
if __name__ == "__main__":
    import random
    
    TEST_STR = "the quick brown fox jumps over the lazy dog"
    shamir = ShamirSharer()
    shares = shamir.share(TEST_STR, 3, 5)
    for s in shares:
        print s.encode("hex")

    for i in range(100):
        shares = shamir.share(TEST_STR, 3, 5)
        samp = random.sample(shares, 3)
        assert shamir.recombine(samp) == TEST_STR
    
    strs = [s.decode("hex") for s in ["0090b9e7ef2119bf791ce62df82068be278cc98338a341199de3a3c9c85a6d650882358ef3f98b686e7ca881",
                                      "010572f3f16c6dd2bef170f26dd8f02936758cf5d7b037d7b893cc0123586afe80bd6b5a59356e94a601bfda",
                                      "02d59489265170a231e8c0afd3950db14d21b9cdfc9157a5c1849b19895f69eadb180685a01723fdc8f5b471"]]
    print shamir.recombine(strs)


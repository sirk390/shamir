from shamir.polynomial import Polynomial, LagrangePolynomial
from shamir.field import ZpField, ZpRandom
from shamir.utils import iterslices, joinbase, splitbase
from struct import pack, unpack

class SecretSharer(object):
    def __init__(self, field, random=None):
        self.field = field
        self.random = random
   
    def share(self, secret, threshold, points):
        coef = [secret]
        coef += [self.random.randitem() for j in range(threshold-1)]
        p = Polynomial(list(reversed(coef)))
        shares = [(pt, p.evaluate(pt)) for pt in points]
        return shares

    def recombine(self, shares, x_recomb):
        xs, ys = zip(*shares)
        p = LagrangePolynomial(shares, self.field.zero(), self.field.one())
        return p.evaluate(x_recomb)

    def recombine_polynomial(self, shares):
        xs, ys = zip(*shares)
        p = LagrangePolynomial(shares, self.field.zero(), self.field.one())
        return p.get_polynomial()

def encode_share(share_idx, values):
    """ values are values from 0 to 256 (just more than 1 byte) """
    res = pack('B', share_idx)
    for group in iterslices(values, 8):
        a = "".join(chr(b) for b in splitbase(joinbase(group, 257), 256))
        #if len(group) != 8:  # last element does not have to be padded to 9 chars
        a = ("\x00" * (9 - len(a)) + a)
        res += a
    return res

def decode_share(share):
    """ values are values from 0 to 256 (just more than 1 byte) """
    share_idx, = unpack('B', share[:1])
    values = []
    for group in iterslices(share[1:], 9):
        values += splitbase(joinbase([ord(c) for c in group], 256), 257)
    return share_idx, values

def share_string(secret_string, threshold, numshares):
    field = ZpField(257)
    V = field.value_type
    sharer = SecretSharer(field, ZpRandom(field))
    all_shares = []
    for c in secret_string:
        shares = sharer.share(V(ord(c)), threshold, [V(i+1) for i in range(numshares)])
        share_values = [value for idx, value in shares]
        all_shares.append(share_values)
    return [encode_share(idx, [s.value for s in shares]) for idx, shares in enumerate(zip(*all_shares))]

def recombine_string(shares):
    field = ZpField(257)
    V = field.value_type
    sharer = SecretSharer(field, ZpRandom(field))
    decoded_shares = [decode_share(s) for s in shares]
    share_zp_indexes = [V(share_idx+1) for share_idx, values in decoded_shares]
    decoded_zp_shares = zip(*[[V(v) for v in values] for share_idx, values in decoded_shares])
    result = ""
    for shares in decoded_zp_shares:
        result += chr(sharer.recombine(zip(share_zp_indexes, shares), V(0)))
    return result
    
if __name__ == "__main__":
    TEST_STR = "the quick brown fox jumps over the lazy dog"
    shares = share_string(TEST_STR, 3, 5)
    for s in shares:
        print s.encode("hex")
    print [len(s) for s in shares], len(TEST_STR)
    
    shares2 = ["000028684ba2d1f18a530076ec6eeb3a7cf97b007c8cd8c0673d596500d48d8b585caf4f0800472a3f2c943a25a4e80b08",
              "03007296cc11b2afdd90002ecba220e61dd5fa0091dfe310c8650a3d003ecd72e5d9db5b0200d0a6a5974a242da0e8fab9",
              "0200aa751fcbe05423130056c2b468f4825a8e000ccbe6957449e86d00b8cbe99f5a15ee9700fe6b2a859f6bb28da869c6",
              ]
    print recombine_string(shares)
    #print recombine_string([s.decode("hex") for s in shares])
    #print decode_share('0000b534443c0f50a0e700f47669e0601b77bd00ddc3b04bbd10805d00ddbf33881051e8c40059f0847bc557f968bc31c6'.decode("hex"))



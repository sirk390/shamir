from polynomial import Polynomial, PointSet
from field import ZpField
from struct import pack, unpack
from random_source import SecureRandomSource
from utils import iterslices, joinbase, splitbase
import collections
import struct

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

class EncodingError(Exception):
    pass

def pack_varint(value):
    """ Pack an integer in such a way that small values take less space (similar to bitcoin encoding but big-endian) """ 
    if (value < 0xfd):
        return (struct.pack("B", value))
    if (value <= 0xffff):
        return ("\xfd" + struct.pack(">H", value))
    if (value <= 0xffffffff):
        return ("\xfe" + struct.pack(">I", value))
    return ("\xff" + struct.pack(">Q", value))
        
def unpack_varint(data, cursor=0):
    """ unpack a integer packed by pack_varint """ 
    prefix = struct.unpack_from(">B", data, cursor)[0]
    cursor += 1
    if (prefix < 0xFD):
        return (prefix, cursor)
    if (len(data) - cursor < {0xFD: 2, 0xFE: 4, 0xFF: 8}[prefix]):
        raise EncodingError("Decoding error: not enough data: %d" % (prefix))
    if (prefix == 0xFD):
        return (struct.unpack_from(">H", data, cursor)[0], cursor + 2)
    if (prefix == 0xFE):
        return (struct.unpack_from(">I", data, cursor)[0], cursor + 4)
    return (struct.unpack_from(">Q", data, cursor)[0], cursor + 8)


def add_padding(str, size=4):
    """ Pad the end of a string to make the length a multiple of 'size'.
     The byte contains the number of characters to remove, to remove the padding.  
     """ 
    nbpad = size - (len(str) % size) 
    return str + (chr(nbpad) * nbpad)

def remove_padding(str):
    """ Remove padding added using 'add_padding' """ 
    nbpad = ord(str[-1])
    return str[:-nbpad]


class ShamirStringSharer(object):
    """ Share and recombine bytestrings by sharing each character separately in GF(257)
        The resulting integers [0-256] are then returned as a bytestring except for 0 and 256 
        that are respectively escaped as '\x00\x00' and '\x00\x01'
    """ 
    def __init__(self, random_source=SecureRandomSource()):
        self.P = 4294967311 # first prime larger than 2**32
        self.field = ZpField(self.P, random_source=random_source)
        self.V = self.field.value_type
        self.sharer = ShamirPointSharer(self.field)
        
    def share(self, secret_string, threshold, numshares):
        assert numshares < self.P, "numshares (%s) must be smaller than P(%s)" % (numshares, self.P)
        assert threshold <= numshares, "threshold (%s) must be smaller or equal to numshares(%s)" % (threshold, numshares)
        all_shares = []
        
        bytevalues = [ord(c) for c in add_padding(secret_string)]
        intvalues = [joinbase(fourbytes, 256) for fourbytes in iterslices(bytevalues, 4)]
        for i in intvalues:
            shares = self.sharer.share(self.V(i), threshold, [self.V(n+1) for n in range(numshares)])
            share_values = [value for idx, value in shares]
            all_shares.append(share_values)
        return [self.encode_share(idx, [s.value for s in shares]) for idx, shares in enumerate(zip(*all_shares))]
        
    def recombine(self, shares):
        decoded_shares = [self.decode_share(s) for s in shares]
        share_zp_indexes = [self.V(share_idx+1) for share_idx, values in decoded_shares]
        decoded_zp_shares = zip(*[[self.V(v) for v in values] for share_idx, values in decoded_shares])
        intvalues = []
        for shares in decoded_zp_shares:
            intvalues.append(self.sharer.recombine(zip(share_zp_indexes, shares), self.V(0)).value)
        bytevalues = []
        for i in intvalues:
            fourbytes = splitbase(i, 256)
            bytevalues += [0] * (4 - len(fourbytes)) + fourbytes
        return remove_padding("".join(chr(b) for b in bytevalues))

    
    def encode_share_values(self, values):
        """ Encodes list of values between 0 and P=4294967311 (smallest prime above 2**32) to bytestrings
            Values from 0 to 2**32-2 take 4 bytes, values above take 5 bytes.
        """
        resbytes = []
        for b in values:
            if b >= 0xffffffff:
                resbytes += [0xff, 0xff, 0xff, 0xff, b - 2**32 + 1]
            else:
                sp = splitbase(b, 256)
                resbytes += [0] * (4-len(sp))
                resbytes += sp
        return "".join(chr(b) for b in resbytes)
        
    def encode_share(self, share_idx, values):
        return pack_varint(share_idx) + self.encode_share_values(values)
    
    def decode_share_values(self, data):
        """ values from 2**32 to P=4294967311 take 5 bytes """
        values = []
        current = []
        chrcodes = collections.deque(ord(c) for c in data)
        while current or chrcodes:
            if chrcodes:
                current.append(chrcodes.popleft())
            if len(current) == 4 and current != [0xff,0xff,0xff,0xff]:
                values.append(joinbase(current, 256))
                current = []
            elif len(current) == 5:
                values.append(2**32 + current[4] - 1)
                current = []
        return values
    
    def decode_share(self, share):
        share_idx, cursor= unpack_varint(share)
        values = self.decode_share_values(share[cursor:])
        return share_idx, values
    

if __name__ == '__main__':

    import random
    shamir = ShamirStringSharer()
    results = shamir.share("hhazeezezzeiokjgtroitrj itiijtr", 3, 10)
    
    for r in results:
        print r.encode("hex")
    #random.sample(results, 400)
    print shamir.recombine(random.sample(results, 3))
    
    exit()
    #print pack_shareidx(10).encode("hex")
    print encode_share(2, [142424242, 4294967295]).encode("hex")
    print encode_share(0, [424242, 4294967296]).encode("hex")
    print encode_share(0, [424242, 4294967310]).encode("hex")
    
    print decode_share("0000067932ffffffff00".decode("hex"))
    
    print 2**32
    #print joinbase([255, 256, 256, 256], 256)
    
    
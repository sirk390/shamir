import unittest
from shamir.shamir import ShamirPointSharer, ShamirStringSharer, pack_varint,\
    unpack_varint
from shamir.field import ZpField
from shamir.polynomial import Polynomial
from shamir.random_source import UnitTestRandomSource


class TestShamir(unittest.TestCase):
    def test_Shamir_Share3OutOf7_ResultIsSharedCorrectly(self):
        field = ZpField(37, UnitTestRandomSource(range(2)))
        V = field.value_type
        numshares = 7
        sharer = ShamirPointSharer(field) # 3 numbers are required for threshold=3
        
        shares = sharer.share(V(12), 3, [V(i+1) for i in range(numshares)])
        
        self.assertEquals(shares,
                          [(V(1), V(13)), 
                           (V(2), V(16)), 
                           (V(3), V(21)), 
                           (V(4), V(28)), 
                           (V(5), V(0)), 
                           (V(6), V(11)), 
                           (V(7), V(24))])
        
    def test_Shamir_WhenShared3OutOf7SharesAndGiven4Shares_SecretCanBeRecombined(self):
        field = ZpField(37)
        V = field.value_type
        recombiner = ShamirPointSharer(field)
        
        secret = recombiner.recombine([(V(2), V(16)), 
                                   (V(7), V(24)),
                                   (V(5), V(0)), 
                                   (V(4), V(28))], x_recomb=V(0))
        
        self.assertEquals(secret,
                          V(12))

    def test_Shamir_WhenShared3OutOf7SharesAndGiven4Shares_PolynomialCanBeRecombined(self):
        field = ZpField(37)
        V = field.value_type
        recombiner = ShamirPointSharer(field)

        polynom = recombiner.recombine_polynomial([(V(2), V(16)), 
                                                   (V(7), V(24)),
                                                   (V(5), V(0)), 
                                                   (V(4), V(28))])
        
        self.assertEquals(polynom, Polynomial([V(0), V(1), V(0), V(12)]))
        
    
    def test_Shamir_WhenShared3OutOf7SharesAndGiven5Shares_SecretCanBeRecombined(self):
        field = ZpField(37)
        V = field.value_type
        sharer = ShamirPointSharer(field)
        

        secret = sharer.recombine([(V(6), V(11)), 
                                   (V(2), V(16)),
                                   (V(4), V(28)), 
                                   (V(7), V(24)), 
                                   (V(5), V(0))], x_recomb=V(0))

    def test_Shamir_WhenShared3OutOf7SharesAndGiven6Shares_SecretCanBeRecombined(self):
        field = ZpField(37)
        V = field.value_type
        sharer = ShamirPointSharer(field)

        secret = sharer.recombine([(V(6), V(11)), 
                                   (V(2), V(16)),
                                   (V(3), V(21)), 
                                   (V(4), V(28)), 
                                   (V(7), V(24)), 
                                   (V(5), V(0))], x_recomb=V(0))
        
        self.assertEquals(secret, V(12))
        
    def test_Shamir_WhenShared3OutOf7SharesAndGiven3Shares_SecretCanBeRecombined(self):
        field = ZpField(37)
        V = field.value_type
        sharer = ShamirPointSharer(field)
        
        secret = sharer.recombine([(V(2), V(16)),
                                   (V(4), V(28)), 
                                   (V(5), V(0))], x_recomb=V(0))
        
    def test_Shamir_WhenShared3OutOf7SharesAndGiven2Shares_ResultIsRandom(self):
        field = ZpField(37)
        V = field.value_type
        sharer = ShamirPointSharer(field)
        
        secret = sharer.recombine([(V(2), V(16)),
                                   (V(4), V(28))], x_recomb=V(0))
        
        self.assertEquals(secret, V(4))
        
    def test_shamir_share_string(self):
        shamir = ShamirStringSharer( random_source=UnitTestRandomSource(range(50)))
        
        shared_strings = shamir.share("the quick brown fox jumps over the lazy dog", 2, 3)
        shared_strings_hex = [e.encode("hex") for e in shared_strings]
        
        self.assertEquals(shared_strings_hex, 
                          ["0074686520717569646b2062746f776e23666f78246a756d7573206f7c6572207b68652074617a7929646f670b",
                           "0174686520717569656b2062766f776e26666f78286a756d7a73206f82657220826865207c617a7932646f6715",
                           "0274686520717569666b2062786f776e29666f782c6a756d7f73206f886572208968652084617a793b646f671f"])
        
    def test_Shamir_ShareString2OutOf3_ResultIsFixed(self):
        """ testcase from fake random 2 out of 3"""
        shamir = ShamirStringSharer()
        
        data = ["0074686520717569646b2062746f776e23666f78246a756d7573206f7c6572207b68652074617a7929646f670b",
                "0174686520717569656b2062766f776e26666f78286a756d7a73206f82657220826865207c617a7932646f6715"]
    
        result =  shamir.recombine([i.decode("hex") for i in data])
        
        self.assertEquals(result, "the quick brown fox jumps over the lazy dog")

    def test_Shamir_WhenSharingString2OutOf3WithFakeRandomAndGiven2Shares_ResultIsCorrect(self):
        """ testcase from fake random 2 out of 3 (2 other values)"""
        shamir = ShamirStringSharer()
        
        data = ["0174686520717569656b2062766f776e26666f78286a756d7a73206f82657220826865207c617a7932646f6715",
                "0274686520717569666b2062786f776e29666f782c6a756d7f73206f886572208968652084617a793b646f671f"]
    
        result =  shamir.recombine([i.decode("hex") for i in data])
        
        self.assertEquals(result, "the quick brown fox jumps over the lazy dog")

    def test_Shamir_WhenSharingString2OutOf3WithRealRandomAndGiven3Shares_ResultIsCorrect(self):
        """ testcase created with real random """
        shamir = ShamirStringSharer()

        data = ["00088e5d07bd3cf928c01870bdad820e3c89cd4c91f6712e0203b83e5aa1b2aa4a97b2b7b9f959822a80b5c22c",
                "019cb454fd090488de15107ef9eb8cae58ad2b2102826cee8594500d4dddf33420c7004f0691388b259cfc1d57",
                "0230da4ce454cc18a36a088d4429974e65d088f5730e68af0824e7dc311a33bde7f64de65329179420b9427882"]
    
        result =  shamir.recombine([i.decode("hex") for i in data])
        
        self.assertEquals(result, "the quick brown fox jumps over the lazy dog")

    def test_Shamir_EncodeShareValues(self):
        shamir = ShamirStringSharer()

        self.assertEquals(shamir.encode_share_values([0]).encode("hex"), "00000000")
        self.assertEquals(shamir.encode_share_values([1]).encode("hex"), "00000001")
        self.assertEquals(shamir.encode_share_values([1000]).encode("hex"), "000003e8")
        self.assertEquals(shamir.encode_share_values([1000000]).encode("hex"), "000f4240")
        self.assertEquals(shamir.encode_share_values([2**32-1]).encode("hex"), "ffffffff00")
        self.assertEquals(shamir.encode_share_values([2**32]).encode("hex"), "ffffffff01")
        self.assertEquals(shamir.encode_share_values([2**32+10]).encode("hex"), "ffffffff0b")
        self.assertEquals(shamir.encode_share_values([2**32+40]).encode("hex"), "ffffffff29")
        self.assertEquals(shamir.encode_share_values([1000, 2**32+40]).encode("hex"), "000003e8ffffffff29")
        self.assertEquals(shamir.encode_share_values([0, 1, 1000, 2**32-2, 2**32-1, 2**32+40]).encode("hex"), "0000000000000001000003e8fffffffeffffffff00ffffffff29")
        self.assertEquals(shamir.encode_share_values([ 2**32+40, 0, 2**32-1, 1, 1000, 2**32-2]).encode("hex"), "ffffffff2900000000ffffffff0000000001000003e8fffffffe")
        

    def test_Shamir_DecodeShareValues(self):
        shamir = ShamirStringSharer()

        self.assertEquals(shamir.decode_share_values('00000000'.decode("hex")), [0])
        self.assertEquals(shamir.decode_share_values('000003e8'.decode("hex")), [1000])
        self.assertEquals(shamir.decode_share_values('000f4240'.decode("hex")), [1000000])
        self.assertEquals(shamir.decode_share_values('ffffffff00'.decode("hex")), [2**32-1])
        self.assertEquals(shamir.decode_share_values('ffffffff01'.decode("hex")), [2**32])
        self.assertEquals(shamir.decode_share_values('ffffffff0b'.decode("hex")), [2**32+10])
        self.assertEquals(shamir.decode_share_values('ffffffff29'.decode("hex")), [2**32+40])
        self.assertEquals(shamir.decode_share_values('000003e8ffffffff29'.decode("hex")), [1000, 2**32+40])
        self.assertEquals(shamir.decode_share_values('0000000000000001000003e8fffffffeffffffff00ffffffff29'.decode("hex")), [0, 1, 1000, 2**32-2, 2**32-1, 2**32+40])
        self.assertEquals(shamir.decode_share_values('ffffffff2900000000ffffffff0000000001000003e8fffffffe'.decode("hex")), [2**32+40, 0, 2**32-1, 1, 1000, 2**32-2])


    def test_Shamir_PackVarInt(self):
        self.assertEquals(pack_varint(0).encode("hex"), "00")
        self.assertEquals(pack_varint(1).encode("hex"), "01")
        self.assertEquals(pack_varint(100).encode("hex"), "64")
        self.assertEquals(pack_varint(200).encode("hex"), "c8")
        self.assertEquals(pack_varint(252).encode("hex"), "fc")
        self.assertEquals(pack_varint(253).encode("hex"), "fd00fd")
        self.assertEquals(pack_varint(254).encode("hex"), "fd00fe")
        self.assertEquals(pack_varint(255).encode("hex"), "fd00ff")
        self.assertEquals(pack_varint(256).encode("hex"), "fd0100")
        self.assertEquals(pack_varint(65535).encode("hex"), "fdffff")
        self.assertEquals(pack_varint(65536).encode("hex"), "fe00010000")
        self.assertEquals(pack_varint(2**32-1).encode("hex"), "feffffffff")
        self.assertEquals(pack_varint(2**32).encode("hex"), "ff0000000100000000")
        self.assertEquals(pack_varint(2**32+1000000000).encode("hex"), "ff000000013b9aca00")

    def test_Shamir_UnpackVarInt(self):
        self.assertEquals(unpack_varint("00".decode("hex")), (0, 1)) # returns (value, nbparsed)
        self.assertEquals(unpack_varint("01".decode("hex")), (1, 1))
        self.assertEquals(unpack_varint("64".decode("hex")), (100, 1))
        self.assertEquals(unpack_varint("c8".decode("hex")), (200, 1))
        self.assertEquals(unpack_varint("fc".decode("hex")), (252, 1))
        self.assertEquals(unpack_varint("fd00fd".decode("hex")), (253, 3))
        self.assertEquals(unpack_varint("fd00fe".decode("hex")), (254, 3))
        self.assertEquals(unpack_varint("fd00ff".decode("hex")), (255, 3))
        self.assertEquals(unpack_varint("fd0100".decode("hex")), (256, 3))
        self.assertEquals(unpack_varint("fdffff".decode("hex")), (65535, 3))
        self.assertEquals(unpack_varint("fe00010000".decode("hex")), (65536, 5))
        self.assertEquals(unpack_varint("feffffffff".decode("hex")), (2**32-1, 5))
        self.assertEquals(unpack_varint("ff0000000100000000".decode("hex")), (2**32, 9))
        self.assertEquals(unpack_varint("ff000000013b9aca00".decode("hex")), (2**32+1000000000, 9))

        
    

if __name__ == "__main__":
    unittest.main()

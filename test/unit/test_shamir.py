import unittest
import itertools
from shamir.shamir import ShamirPointSharer, ShamirSharer, decode_share
from shamir.field import ZpField
from shamir.polynomial import Polynomial
from shamir.random_source import UnitTestRandomSource
import collections


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

    def test_Shamir_WhenSharing1Byte2OutOf3_ShamirProvidesPerfectSecrecy(self):
        """ Tests perfect secrecy for 1 shared byte, and k=2, n=3.
         
            When iterating over all possible random values and encoding each possible output, yields all combination once, 
            thus the algorithm provides perfect secrecy if the random source is secure.
        """
        shamir = ShamirSharer( random_source=UnitTestRandomSource(itertools.cycle(range(257))))
        
        share1_counts = collections.Counter()
        share2_counts = collections.Counter()
        share3_counts = collections.Counter()

        for b in range(256): # iterate over all encodable byte values
            for r in range(257): # iterate over all random values 
                sharedbyte = shamir.share(chr(b), 2, 3)
                share1_counts[(b, decode_share(sharedbyte[0])[1][0])] += 1
                share2_counts[(b, decode_share(sharedbyte[1])[1][0])] += 1
                share3_counts[(b, decode_share(sharedbyte[2])[1][0])] += 1

        for b in range(256): # iterate over all encodable byte values
            for r in range(257): # iterate over all random values 
                self.assertEquals(share1_counts[(b, r)], 1)
                self.assertEquals(share2_counts[(b, r)], 1)
                self.assertEquals(share3_counts[(b, r)], 1)
        
    def test_shamir_share_string(self):
        shamir = ShamirSharer( random_source=UnitTestRandomSource(range(50)))
        
        shared_strings = shamir.share("the quick brown fox jumps over the lazy dog", 2, 3)
        shared_strings_hex = [e.encode("hex") for e in shared_strings]
        
        self.assertEquals(shared_strings_hex, 
                          ["0074696723757a6f6a73296c7d7b847c2f76808a337e8a83878b398991818f3e938886428f859f9f478c9891",
                           "01746a6926797f75717b32768887918a3e86919c46929f999ea352a3ac9dac5cb2a8a764b2a9c4c56eb4c1bb",
                           "02746b6b297d847b78833b8093939e984d96a2ae59a6b4afb5bb6bbdc7b9c97ad1c8c886d5cde9eb95dceae5"])
        
    def test_Shamir_ShareString2OutOf3_ResultIsFixed(self):
        """ testcase from fake random 2 out of 3"""
        shamir = ShamirSharer()
        
        data = ["0074696723757a6f6a73296c7d7b847c2f76808a337e8a83878b398991818f3e938886428f859f9f478c9891",
                "01746a6926797f75717b32768887918a3e86919c46929f999ea352a3ac9dac5cb2a8a764b2a9c4c56eb4c1bb"]
    
        result =  shamir.recombine([i.decode("hex") for i in data])
        
        self.assertEquals(result, "the quick brown fox jumps over the lazy dog")

    def test_Shamir_WhenSharingString2OutOf3WithFakeRandomAndGiven2Shares_ResultIsCorrect(self):
        """ testcase from fake random 2 out of 3 (2 other values)"""
        shamir = ShamirSharer()
        
        data = ["01746a6926797f75717b32768887918a3e86919c46929f999ea352a3ac9dac5cb2a8a764b2a9c4c56eb4c1bb",
                "02746b6b297d847b78833b8093939e984d96a2ae59a6b4afb5bb6bbdc7b9c97ad1c8c886d5cde9eb95dceae5"]
    
        result =  shamir.recombine([i.decode("hex") for i in data])
        
        self.assertEquals(result, "the quick brown fox jumps over the lazy dog")

    def test_Shamir_WhenSharingString2OutOf3WithRealRandomAndGiven3Shares_ResultIsCorrect(self):
        """ testcase created with real random """
        shamir = ShamirSharer()
        
        data = ["0090b9e7ef2119bf791ce62df82068be278cc98338a341199de3a3c9c85a6d650882358ef3f98b686e7ca881",
                "010572f3f16c6dd2bef170f26dd8f02936758cf5d7b037d7b893cc0123586afe80bd6b5a59356e94a601bfda",
                "02d59489265170a231e8c0afd3950db14d21b9cdfc9157a5c1849b19895f69eadb180685a01723fdc8f5b471"]
    
        result =  shamir.recombine([i.decode("hex") for i in data])
        
        self.assertEquals(result, "the quick brown fox jumps over the lazy dog")


if __name__ == "__main__":
    unittest.main()

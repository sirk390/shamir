import unittest
import itertools
from shamir.shamir import ShamirPointSharer, ShamirStringSharer, pack_varint,\
    unpack_varint
from shamir.field import ZpField
from shamir.polynomial import Polynomial
from shamir.random_source import UnitTestRandomSource
import collections


class TestShamirSlow(unittest.TestCase):
    def test_shamir_share_string_many_shares(self):
        shamir = ShamirStringSharer( random_source=UnitTestRandomSource(range(5000)))
        
        shared_strings = shamir.share("abcd", 500, 1000)
        shared_strings_hex = [e.encode("hex") for e in shared_strings]
        print len(shared_strings)
        self.assertEquals(shared_strings_hex[-3:], 
                          ["fd03e5fb1f47b53999f54a",
                           "fd03e60142cc5c6b6db0bd",
                           "fd03e7b77b0a13da539d9b"])

    '''
    def test_Shamir_WhenSharing1Byte2OutOf3_ShamirProvidesPerfectSecrecy(self):
        """ Tests perfect secrecy for 1 shared byte, and k=2, n=3.
         
            When iterating over all possible random values and encoding each possible output, yields all combination once, 
            thus the algorithm provides perfect secrecy if the random source is secure.
        """
        shamir = ShamirStringSharer( random_source=UnitTestRandomSource(itertools.cycle(range(257))))
        
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
                self.assertEquals(share3_counts[(b, r)], 1)'''


        
    

if __name__ == "__main__":
    unittest.main()

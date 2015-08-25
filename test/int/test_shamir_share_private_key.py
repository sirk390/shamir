import unittest
from shamir.sharer import SecretSharer
from shamir.recombiner import SecretRecombiner
from shamir.field import ZpField, ZpRandom
from coinpy.tools.ssl.ecdsa import KEY
from coinpy.tools.seeds.system_seeds import ssl_add_system_seeds
from coinpy.lib.transactions.address import BitcoinAddress
from coinpy.model.protocol.runmode import MAIN
import random
from coinpy.tools.hex import hexstr, decodehexstr
from coinpy.tools.bitcoin.base256 import base256encode, base256decode

class TestShamir(unittest.TestCase):
    def test_shamir_share_private_key(self):
        ssl_add_system_seeds()
        k = KEY()
        k.generate()
        pkey_bignum = k.get_privkey_bignum()
        pubkey = k.get_pubkey()
        numshares = 600
        threshold = 100
        sharenum_bytes = 2
        print "private_key_bignum:", pkey_bignum
        print "public_key:", hexstr(pubkey)
        print "address:", BitcoinAddress.from_publickey(pubkey, MAIN)
        
        field = ZpField()
        V = field.value_type
        ZpPkey = V(pkey_bignum)

        sharer = SecretSharer(field, ZpRandom(field))
        shares = sharer.share(ZpPkey, threshold, [V(i+1) for i in range(numshares)])
        # print shares
        print "Shamir Shares: (%d/%d):" % (threshold, numshares)
        shares_hex = [hexstr(base256encode(int(pt), sharenum_bytes) + base256encode(int(value), 32)) for pt, value in shares]
        
        for share in shares_hex:
            print share
        # Try to reconstruct the private key using the hex encoded shares.
        recombiner = SecretRecombiner(field)
        for i in range(10):
            random4_hex = random.sample(shares_hex, threshold)
            random4_decoded = [decodehexstr(h) for h in random4_hex]
            random4 = [(V(base256decode(data[:sharenum_bytes])), V(base256decode(data[sharenum_bytes:]))) for data in random4_decoded]
            recombined_pkey_bignum = recombiner.recombine(random4, V(0))
            assert recombined_pkey_bignum == ZpPkey
            k2 = KEY()
            k2.set_privkey_bignum(int(recombined_pkey_bignum))
            assert k2.get_pubkey() == pubkey
            print i
        # With threshold-1 shares this fails
        for i in range(10):
            random4_hex = random.sample(shares_hex, threshold-1)
            random4_decoded = [decodehexstr(h) for h in random4_hex]
            random4 = [(V(base256decode(data[:sharenum_bytes])), V(base256decode(data[sharenum_bytes:]))) for data in random4_decoded]
            recombined_pkey_bignum = recombiner.recombine(random4, V(0))
            assert recombined_pkey_bignum != ZpPkey

if __name__ == "__main__":
    unittest.main()

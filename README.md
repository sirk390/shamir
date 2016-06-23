This library provides implements the Shamir Secret Sharing Algorithm.
The maximum values of K and N are 4294967310.

The details algorithm used is the following:

The input string (which may be binary) is padded to a length of modulo 4 bytes, each four bytes of the input is shared in GF(4294967311). The resulting secret is than the share index encoded as a variable size integer (values lower than 253 take 1 byte, values lower than 65535 take 3 bytes, other values take 5 bytes) concatenated with the resulting points encoded using 4 or 5 bytes (5 bytes are used when the value is larger than 2**32-2). 

Example usage:
--------------   

Sharing a binary string
***********************

Below is an example usage for k=2 and n=3:

    >>> from shamir.shamir import ShamirStringSharer
    >>> shamir = ShamirStringSharer()
    >>> secrets = shamir.share("the quick brown fox jumps over the lazy dog", 2, 3)
    >>> for secret in secrets:
    >>>     print secret.encode("hex")
    00993d36fd2bbf51db8db8fbff596815a680bf353bd7e69f87bf65359bf0927dda3ae752b7db5bfd677b52318f
    01be1208dae6093a62b051958c4358bd2c9b0ef2564557d18f0ba9fbb17bb2db310d698502553d819f9234fc1d
    02e2e6dab7a05322dad2ea2f192d4964b2b55eaf71b2c903a657eec1d606d33888dfebb75ccf1f05e6a917c6ab

Recombining the shares
***************************
    >>> from shamir.shamir import ShamirStringSharer
    >>> shamir = ShamirStringSharer()
    >>> secrets = ["00993d36fd2bbf51db8db8fbff596815a680bf353bd7e69f87bf65359bf0927dda3ae752b7db5bfd677b52318f",
                   "01be1208dae6093a62b051958c4358bd2c9b0ef2564557d18f0ba9fbb17bb2db310d698502553d819f9234fc1d"]
    >>> print shamir.recombine([secret.decode("hex") for secret in secrets])
    "the quick brown fox jumps over the lazy dog"



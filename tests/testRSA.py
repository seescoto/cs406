import unittest
from src import schemes


class tests(unittest.TestCase):

    def test(self):
        # generates p, q randomly - get N, e, d
        p, q, N, e, d = schemes.getKeysRSA()
        ms = list(range(2, N-1))
        cs = [schemes.RSA(m, e, N) for m in ms]
        mPrimes = [schemes.RSA(c, d, N) for c in cs]

        # assert are the same
        self.assertTrue(ms == mPrimes)


if __name__ == '__main__':
    unittest.main()

import unittest
from src import util


class tests(unittest.TestCase):

    plaintext = "hello! nice to meet you."
    intPlaintext = util.toIntArray(plaintext, False)

    key = "hey"
    intKey = util.toIntArray(key, False)

    def test(self):
        # tests plaintext and key
        # encrypt, decrypt
        intCipher = util.PRP(self.intKey, self.intPlaintext)
        intDecrypted = util.PRPinv(self.intKey, intCipher)

        # assert
        self.assertTrue(intDecrypted == self.intPlaintext)


if __name__ == '__main__':
    unittest.main()

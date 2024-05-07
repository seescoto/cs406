import unittest
from src import util

class tests(unittest.TestCase):

    plaintext = "hello! nice to meet you."
    binPlaintext = util.stringToBinaryString(plaintext)

    key = "hey"
    binKey = util.stringToBinaryString(key)

    def testbb(self):
        # tests binary plaintext and binary key
        # encrypt, decrypt
        binCipher = util.PRP(self.binKey, self.binPlaintext, binK=True, binV=True)
        binDecryptedCipher = util.PRPinv(self.binKey, binCipher, binK = True, binV = True)

        # assert
        self.assertTrue(binDecryptedCipher == self.binPlaintext)

    def testbr(self):
        # tests binary plaintext and regular (character string) key 
        # encrypt, decrypt 
        binCipher = util.PRP(self.key, self.binPlaintext, binK=False, binV=True) 
        binDecryptedCipher = util.PRPinv(self.key, binCipher, binK=False, binV=True)

        # assert
        self.assertTrue(binDecryptedCipher == self.binPlaintext)

    def testrb(self):
        # tests regular (char string) plaintext and binary key 
        # encrypt, decrypt 
        cipher = util.PRP(self.binKey, self.plaintext, binK=True, binV=False)
        decryptedCipher = util.PRPinv(self.binKey, cipher, binK=True, binV=False)

        # assert
        self.assertTrue(decryptedCipher == self.plaintext)

    def testrr(self):
        # tests regular (char string) plaintext and key 
        # encrypt, decrypt 
        cipher = util.PRP(self.key, self.plaintext, binK=False, binV=False) 
        decryptedCipher = util.PRPinv(self.key, cipher, binK=False, binV=False)

        # assert
        self.assertTrue(decryptedCipher == self.plaintext)
    

if __name__ == '__main__':
    unittest.main()

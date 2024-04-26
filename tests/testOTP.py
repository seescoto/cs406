import unittest
from src import schemes, util

# tests that OTP() works with all input types (binary string and regular string)


class tests(unittest.TestCase):

    plaintext = "hello! nice to meet you."
    binPlaintext = util.stringToBinaryString(plaintext)

    key = "hey"
    binKey = util.stringToBinaryString(key)

    def testbb(self):
        # tests binary plaintext and binary key
        # encrypt, decrypt
        binCipher = schemes.OTP(
            self.binPlaintext, self.binKey, binaryPT=True, binaryKey=True)
        binDecryptedCipher = schemes.OTP(
            binCipher, self.binKey, binaryPT=True, binaryKey=True)

        # convert to char string and assert
        decryptedCipher = util.binaryStringToString(binDecryptedCipher)
        self.assertTrue(decryptedCipher == self.plaintext)

    def testbr(self):
        # tests binary plaintext and regular (character) key
        binCipher = schemes.OTP(
            self.binPlaintext, self.key, binaryPT=True, binaryKey=False)
        binDecryptedCipher = schemes.OTP(
            binCipher, self.key, binaryPT=True, binaryKey=False)

        # convert to char string and assert
        decryptedCipher = util.binaryStringToString(binDecryptedCipher)
        self.assertTrue(decryptedCipher == self.plaintext)

    def testrb(self):
        # tests regular (character) plaintext and binary key
        binCipher = schemes.OTP(
            self.plaintext, self.binKey, binaryPT=False, binaryKey=True)
        binDecryptedCipher = schemes.OTP(
            binCipher, self.binKey, binaryPT=True, binaryKey=True)

        # convert to char string and assert
        decryptedCipher = util.binaryStringToString(binDecryptedCipher)
        self.assertTrue(decryptedCipher == self.plaintext)

    def testrr(self):
        # tests regular (character) plaintext and regular (character) key
        binCipher = schemes.OTP(self.plaintext, self.key,
                                binaryPT=False, binaryKey=False)
        binDecryptedCipher = schemes.OTP(
            binCipher, self.key, binaryPT=True, binaryKey=False)

        # convert to char string and assert
        decryptedCipher = util.binaryStringToString(binDecryptedCipher)
        self.assertTrue(decryptedCipher == self.plaintext)


if __name__ == '__main__':
    unittest.main()

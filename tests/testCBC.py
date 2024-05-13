import unittest
from src import schemes, util


class tests(unittest.TestCase):

    plaintext = "hello! nice to meet you."
    binPlaintext = util.stringToBinaryString(plaintext)

    key = "hey"
    binKey = util.stringToBinaryString(key)

    def testbb(self):
        # tests binary plaintext and binary key
        # encrypt, decrypt
        binCipher = schemes.encryptCBC(
            self.binKey, self.binPlaintext, binK=True, binM=True)
        binDecryptedCipher = schemes.decryptCBC(
            self.binKey, binCipher, binK=True, binC=True)
        decrypted = util.binaryStringToString(binDecryptedCipher)

        # assert
        self.assertTrue(decrypted == self.plaintext)

    def testbr(self):
        # tests binary plaintext and regular (character string) key
        # encrypt, decrypt
        binCipher = schemes.encryptCBC(
            self.key, self.binPlaintext, binK=False, binM=True)
        binDecryptedCipher = schemes.decryptCBC(
            self.key, binCipher, binK=False, binC=True)
        decrypted = util.binaryStringToString(binDecryptedCipher)

        # assert
        self.assertTrue(decrypted == self.plaintext)

    def testrb(self):
        # tests regular (char string) plaintext and binary key
        # encrypt, decrypt
        binCipher = schemes.encryptCBC(
            self.binKey, self.plaintext, binK=True, binM=False)
        binDecryptedCipher = schemes.decryptCBC(
            self.binKey, binCipher, binK=True, binC=True)
        decrypted = util.binaryStringToString(binDecryptedCipher)

        # assert
        self.assertTrue(decrypted == self.plaintext)

    def testrr(self):
        # tests regular (char string) plaintext and key
        # encrypt, decrypt
        binCipher = schemes.encryptCBC(
            self.key, self.plaintext, binK=False, binM=False)
        binDecryptedCipher = schemes.decryptCBC(
            self.key, binCipher, binK=False, binC=True)

        decrypted = util.binaryStringToString(binDecryptedCipher)
        # assert
        self.assertTrue(decrypted == self.plaintext)


if __name__ == '__main__':
    unittest.main()

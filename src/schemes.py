# use this if running via flask otherwise get 'no module named util' error
from . import util

# import util  # use this if running schemes.py via terminal


def XOR(arr1, arr2):
    # XOR two arrays of integers
    if len(arr1) != len(arr2):
        raise ValueError("Arrays are not the same length, can't be XORED")

    return [arr1[i] ^ arr2[i] for i in range(len(arr1))]


def OTP(plaintext, key, binaryPT=False, binaryKey=False):
    # takes a key and a plaintext and XORS them to create the encrypted ciphertext
    # binaryPT and binaryKey are bool variables that says if the plaintext/key is in binary format or a reg string

    # if no key given, return none
    if not key:
        return None

    # transform plaintext and key into integers so can be XORed
    intPlain, intKey = util.convert(plaintext, key, binaryPT, binaryKey)
    # match length key to plaintext
    intKey = util.matchLength(intKey, len(intPlain))

    intCipher = XOR(intPlain, intKey)
    # return binary string of ciphertext
    return util.intArrayToBinaryString(intCipher)


def ratchet(key, loops=1, binary=False):
    # convert key to int array
    if binary:
        s = util.binaryStringToIntArray(key)
    else:
        s = util.stringToIntArray(key)
    halfway = len(s)  # index to split s and t

    # double length of int array w/ prg, then split into s_i and t_i
    # t_i is new key, s_i generates next key
    for _ in range(loops):
        total = util.PRG(s)
        s = total[0:halfway]
        t = total[halfway:]

    return (s, t)


# binary key, string plaintext
'''
binKey = util.stringToBinaryString("hey")
plain = "hello my name is sofia"
cipher = OTP(plain, binKey, binaryKey=True)
print(util.binaryStringToString(OTP(cipher, binKey, binaryPT=True, binaryKey=True)))
'''

# string key, string plaintext
'''
k = 'hey'
plain = 'hello my name is sofia'
cipher = OTP(plain, k)
print(util.binaryStringToString(OTP(cipher, k, binaryPT=True)))
'''

# string key, binary plaintext
"""
k = 'hey'
binPlain = util.stringToBinaryString("hello my name is sofia")
cipher = OTP(binPlain, k, binaryPT=True)
print(util.binaryStringToString(OTP(cipher, k, binaryPT=True, binaryKey=False)))
"""


# binary key, binary plaintext
'''
binKey = util.stringToBinaryString("hey")
binPlain = util.stringToBinaryString("hello my name is sofia")
cipher = OTP(binPlain, binKey, binaryPT=True, binaryKey=True)
print(util.binaryStringToString(OTP(cipher, binKey, binaryPT=True, binaryKey=True)))
'''

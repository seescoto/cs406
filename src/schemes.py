# use this if running via flask otherwise get 'no module named util' error
from . import util

# import util  # use this if running schemes.py via terminal


def OTP(plaintext, key, binaryPT=False, binaryKey=False):
    # takes a key and a plaintext and XORS them to create the encrypted ciphertext
    # binaryPT and binaryKey are bool variables that says if the plaintext/key is in binary format or a reg string

    # if no key given, return none
    if not key:
        return None

    # transform plaintext and key into integers so can be XORed
    intPlain = util.toIntArray(plaintext, binaryPT)
    intKey = util.toIntArray(key, binaryKey)
    # match length key to plaintext
    intKey = util.matchLength(intKey, len(intPlain))

    intCipher = util.XOR(intPlain, intKey)
    # return binary string of ciphertext
    return util.intArrayToBinaryString(intCipher)


def ratchet(key, loops=1, binary=False):
    # convert key to int array
    s = util.toIntArray(key, binary)
    halfway = len(s)  # index to split s and t

    # double length of int array w/ prg, then split into s_i and t_i
    # t_i is new key, s_i generates next key
    for _ in range(loops):
        total = util.PRG(s)
        s = total[0:halfway]
        t = total[halfway:]

    return (s, t)

# use this if running via flask otherwise get 'no module named util' error
from . import util
import random

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


blen = 4


def encryptCBC(k, m, binK=False, binM=False):
    """CBC block chaining

    Args:
        k (string): string (char or binary) that represents the key
        m (string): string (char or binary) that represents the plaintext message
        binK (bool, optional): true if k is a binary string. Defaults to False.
        binM (bool, optional): true if m is a binary string. Defaults to False.

    Returns:
        encrypted message c as a binary string 
    """
    m = util.toIntArray(m, binM)
    k = util.toIntArray(k, binK)

    # split m into into n blocks of length blen
    # if m has indivisible length to blen, add spaces to the end
    m = util.addToNoRemainder(m, ord(" "), blen)
    blocks = len(m)//blen
    m = util.stringSplit(m, blocks)

    # encrypted ciphertext in blocks of length blen + 1 for initialization vector
    c = [[0] * blen] * (blocks + 1)
    c[0] = [random.randint(0, 256)
            for _ in range(blen)]  # initialization vector

    # each block c[i] is the resulf of F(k, m[i-1] XOR c[i-1])
    for i in range(1, blocks + 1):
        mc = util.XOR(m[i-1], c[i-1])
        c[i] = util.PRP(k, mc)

    # convert c into binary string
    totalCString = [util.intArrayToBinaryString(b) for b in c]
    totalCString = " ".join(totalCString)

    return totalCString


def decryptCBC(k, c, binK=False, binC=False):
    """decrypts ciphertext c with key k

    Args:
        k (int array): key int array
        c (int array): ciphertext int array
        binK (bool, optional): true if k is a binary string. Defaults to False.
        binC (bool, optional): true if c is a binary string. Defaults to False.

    Returns:
        decrypted plaintext message m as binary string 
    """
    # convert to int arrays
    c = util.toIntArray(c, binC)
    k = util.toIntArray(k, binK)

    # split c into blocks of length blen
    blocks = len(c)//blen
    c = util.stringSplit(c, blocks)

    m = [[0] * blen] * (blocks - 1)
    # each block m[i] is the result of F^{-1}(k, c[i+1]) XOR c[i]
    for i in range(len(m)):
        m[i] = util.PRPinv(k, c[i+1])
        m[i] = util.XOR(m[i], c[i])

    # unpack nested list and get rid of spaces added in encryption
    m = util.unpack(m)
    m = util.removeEnding(m, ord(" "))

    # return m as binary string
    return util.intArrayToBinaryString(m)

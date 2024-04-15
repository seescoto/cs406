from . import util
# import util


def XOR(arr1, arr2):
    # XOR two arrays of integers
    if len(arr1) != len(arr2):
        raise ValueError("Arrays are not the same length, can't be XORED")

    return [arr1[i] ^ arr2[i] for i in range(len(arr1))]


def OTP(plaintext, key, binary=False):
    # takes a key and a plaintext and XORS them to create the encrypted ciphertext
    # binary is a bool variable that says if the plaintext is in binary format or in text

    # if no key given, return none
    if not key:
        return None

    # transform plaintext and key into integers so can be XORed
    if binary:
        intPlain = util.binaryStringToIntArray(plaintext)
    else:
        intPlain = util.stringToIntArray(plaintext)

    intKey = util.stringToIntArray(util.matchLength(key, len(intPlain)))
    intCipher = XOR(intPlain, intKey)
    binCipher = util.intArrayToBinaryString(intCipher)

    return binCipher


# not working, giving weird non consistent answers
# OTP(c, k) here prints m[1:] not m (so the message without the first letter), but it says they're equal??

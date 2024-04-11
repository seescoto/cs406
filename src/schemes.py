import util


def XOR(arr1, arr2):
    # XOR two arrays of integers
    if len(arr1) != len(arr2):
        raise ValueError("Arrays are not the same length, can't be XORED")

    return [arr1[i] ^ arr2[i] for i in range(len(arr1))]


def OTP(plaintext, key):
    # takes a key and a plaintext and XORS them to create the encrypted ciphertext

    # if no key given, return none
    if not key:
        return None

    # transform plaintext and key into integers so can be XORed
    intPlain = util.stringToIntArray(plaintext)
    intKey = util.stringToIntArray(util.matchLength(key, len(plaintext)))
    intCipher = XOR(intPlain, intKey)
    stringCipher = util.intArrayToString(intCipher)

    return stringCipher


m = 'hello my name is sofia escoto'
k = 'h'
c = OTP(m, k)
print(c)
print(OTP(c, k))
print(m)
print(OTP(c, k) == m)


# not working, giving weird non consistent answers
# OTP(c, k) here prints m[1:] not m (so the message without the first letter, h), but it says they're equal??

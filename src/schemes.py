# use this if running via flask otherwise get 'no module named util' error
from . import util
import random

# import util  # use this if running schemes.py via terminal

blen = 4  # global variable for all block ciphers


def OTP(plaintext, key, binaryPT=False, binaryKey=False):
    """OTP scheme - takes a plaintext and key and XOR's them to generate encrypted ciphertext.

    Args:
        plaintext (str): message to be encrypted
        key (str): key value
        binaryPT (bool, optional): true if plaintext is a binary string, false if character string. Defaults to False.
        binaryKey (bool, optional): true if key is a binary string, false if character string. Defaults to False.

    Returns:
        ciphertext (str) : binary string of ciphertext
    """

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
    """generates new keys using symmetric ratchet scheme (length doubling PRG)

    Args:
        key (str): original key, binary or character string
        loops (int, optional): number of loops to go through in ratchet. Defaults to 1.
        binary (bool, optional): true if key is a binary string, false if character string. Defaults to False.

    Returns:
        s, t (int arr, int arr): s is generator for next new key, t is new key
    """
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


def encryptCBC(k, m, binK=False, binM=False):
    """CBC block chaining encryption

    Args:
        k (string): string (char or binary) that represents the key
        m (string): string (char or binary) that represents the plaintext message
        binK (bool, optional): true if k is a binary string. Defaults to False.
        binM (bool, optional): true if m is a binary string. Defaults to False.

    Returns:
        encrypted message c as a binary string 
    """
    # prepare - convert to int arrays, find # blocks, split m into blocks of length blen
    m, k, blocks = util.prepareBC(m, k, binM, binK, blen)

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
    """decrypts ciphertext c with key k in CBC block chaining

    Args:
        k (int array): key int array
        c (int array): ciphertext int array
        binK (bool, optional): true if k is a binary string. Defaults to False.
        binC (bool, optional): true if c is a binary string. Defaults to False.

    Returns:
        decrypted plaintext message m as binary string 
    """
    # prepare - convert to int arrays, find # blocks, split c into blocks of length blen
    c, k, blocks = util.prepareBC(c, k, binC, binK, blen)

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


def encryptCTR(k, m, binK=False, binM=False):
    """CTR counter block chaining encryption

    Args:
        k (string): string (char or binary) that represents the key
        m (string): string (char or binary) that represents the plaintext message
        binK (bool, optional): true if k is a binary string. Defaults to False.
        binM (bool, optional): true if m is a binary string. Defaults to False.

    Returns:
        encrypted message c as a binary string 
    """
    # prepare - convert to int arrays, find # blocks, split m into blocks of length blen
    m, k, blocks = util.prepareBC(m, k, binM, binK, blen)

    # get initialization vector (IV)
    r = [random.randint(0, 256) for _ in range(blen)]

    # encrypted ciphertext in blocks of length blen + 1 for initialization vector
    c = [[0] * blen] * (blocks + 1)
    c[0] = r  # initialization vector

    # each block c[i+1] is the resulf of F(k, r) XOR m[i]) (r incremented each loop)
    for i in range(blocks):
        Fkr = util.PRP(k, r)
        c[i+1] = util.XOR(Fkr, m[i])
        # increment r
        r = util.addModular(r, 1)

    # convert c into binary string
    totalCString = [util.intArrayToBinaryString(b) for b in c]
    totalCString = " ".join(totalCString)

    return totalCString


def decryptCTR(k, c, binK=False, binC=False):
    """decrypts ciphertext c with key k (CTR block cipher)

    Args:
        k (int array): key int array
        c (int array): ciphertext int array
        binK (bool, optional): true if k is a binary string. Defaults to False.
        binC (bool, optional): true if c is a binary string. Defaults to False.

    Returns:
        decrypted plaintext message m as binary string 
    """
    # prepare - convert to int arrays, find # blocks, split c into blocks of length blen
    c, k, blocks = util.prepareBC(c, k, binC, binK, blen)

    m = [[0] * blen] * (blocks - 1)
    r = c[0]

    # each m[i] = c[i+1] XOR F(k, r)
    for i in range(len(m)):
        Fkr = util.PRP(k, r)
        m[i] = util.XOR(Fkr, c[i+1])
        # increment r
        r = util.addModular(r, 1)

    # unpack nested list and get rid of spaces added in encryption
    m = util.unpack(m)
    m = util.removeEnding(m, ord(" "))

    # return m as binary string
    return util.intArrayToBinaryString(m)


def encryptOFB(k, m, binK=False, binM=False):
    """OFB (output feedback) block chaining encryption

    Args:
        k (string): string (char or binary) that represents the key
        m (string): string (char or binary) that represents the plaintext message
        binK (bool, optional): true if k is a binary string. Defaults to False.
        binM (bool, optional): true if m is a binary string. Defaults to False.

    Returns:
        encrypted message c as a binary string 
    """
    # prepare - convert to int arrays, find # blocks, split m into blocks of length blen
    m, k, blocks = util.prepareBC(m, k, binM, binK, blen)

    # get initialization vector (IV)
    r = [random.randint(0, 256) for _ in range(blen)]

    # encrypted ciphertext in blocks of length blen + 1 for initialization vector
    c = [[0] * blen] * (blocks + 1)
    c[0] = r  # initialization vector

    # each block c[i+1] is the result of F(k, r) XOR m[i] (r is updated each loop to be Fkr)
    for i in range(blocks):
        r = util.PRP(k, r)
        c[i+1] = util.XOR(r, m[i])

    # convert c into binary string
    totalCString = [util.intArrayToBinaryString(b) for b in c]
    totalCString = " ".join(totalCString)

    return totalCString


def decryptOFB(k, c, binK=False, binC=False):
    """decrypts ciphertext c with key k (OFB block cipher)

    Args:
        k (int array): key int array
        c (int array): ciphertext int array
        binK (bool, optional): true if k is a binary string. Defaults to False.
        binC (bool, optional): true if c is a binary string. Defaults to False.

    Returns:
        decrypted plaintext message m as binary string 
    """
    # prepare - convert to int arrays, find # blocks, split m into blocks of length blen
    c, k, blocks = util.prepareBC(c, k, binC, binK, blen)

    # create int array for m and get r = c[0]
    m = [[0] * blen] * (blocks - 1)
    r = c[0]

    # each m[i] is c[i+1] XOR F(k, r) (r is updated to be Fkr each loop)
    for i in range(1, blocks):
        m[i-1] = util.XOR(c[i], util.PRP(k, r))
        r = util.PRP(k, r)

    # unpack nested list and get rid of spaces added in encryption
    m = util.unpack(m)
    m = util.removeEnding(m, ord(" "))

    # return m as binary string
    return util.intArrayToBinaryString(m)


def getKeysRSA(p=None, q=None):
    """given two distinct primes p, and q, return N = p * q and multiplicative inverses e and d 
    such that ( e * d % phi(N) = 1 ) where phi(N) is euler's totient function phi(N) = (p-1)*(q-1)

    Args:
        p (int, optional): prime number such that p != q. defaults to None
        q (int, optional): prime number such that p != q. defaults to None

    Returns:
        (p, q, N, e, d).
        N (int) = p * q,
        e (int) and d (int) are multiplicative inverses so e * d % phi(N) = 1,
        e is the public inverse, d is private

    """
    # if no (or invalid) p, q given, generate them
    if (util.invalidRSAPrimes(p, q)):
        # find p, q, N
        maxNum = 100
        p = util.getPrime(10, maxNum)
        q = util.getPrime(10, maxNum)
        while (q == p):
            q = util.getPrime(maxNum)
    N = p * q

    # get e and d
    phiN = (p-1)*(q-1)
    d = util.getCoPrime(phiN)  # private key
    e = util.getMultInverse(d, phiN)  # public key

    return (p, q, N, e, d)


def RSA(m, e, N):
    """unhashed RSA scheme (not secure! just for educational purposes!)

    Args:
        m (int): message/ciphertext to encrypt/decrypt (integer less than N)
        e (int): key exponent
        N (int): modular value

    Returns:
        c (int): encrypted/decrypted message/ciphertext c = m^e % N
    """
    return util.modExp(m, e, N)

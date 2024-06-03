# utility functions
import re  # regex
import random


def XOR(arr1, arr2):
    # XOR two arrays of integers
    if len(arr1) != len(arr2):
        raise ValueError("Arrays are not the same length, can't be XORED")

    return [arr1[i] ^ arr2[i] for i in range(len(arr1))]


def stringToIntArray(string):
    # make a string into an integer array - each element is the int representation of the character in that index
    # ord(character) transforms a char to the int that it represents in ascii
    return [ord(c) for c in string]


def intArrayToString(arr):
    # makes an int array into a string - each int will be an ascii char
    return "".join([chr(i) for i in arr])


def splitBinaryString(binString):
    if (re.findall(r'\s+', binString)):
        # if contains whitespace, split by whitespace
        binString = binString.split()
    else:
        # else split so each binByte has 8 chars in it
        binString = [binString[i:i+8] for i in range(0, len(binString), 8)]
    return binString


def binaryStringToIntArray(binString):
    # given a string of 0's and 1's (as characters)
    # convert it to an int array where each 'byte' becomes an integer in the array
    return [int(binByte, 2) for binByte in splitBinaryString(binString)]


def intToBinaryString(num):
    # converts an integer into a binary string (separated by spaces)

    # convert, remove '0b' prefix, add 0's to end so it divides 8
    string = bin(num)[2:]  # get rid of '0b' prefix
    remainder = len(string) % 8
    if remainder != 0:
        string = "0"*(8 - remainder) + string

    # deliminate by spaces
    binArr = splitBinaryString(string)
    string = " ".join(binArr)

    return string


def binaryStringToInt(string):
    return int(string.replace(" ", ""), 2)


def intArrayToBinaryString(arr):
    """
    convert int array to binary string

    Args:
        arr (int array)

    Returns:
        str: binary string representing each int in arr as a byte
    """
    # given an int array, convert each int into binary and then return a string of all bytes separated by spaces
    strArr = [bin(i)[2:].zfill(8) for i in arr]
    # zfill 8 so it keeps leading zeros, [2:] so it doesnt put '0b' prefix into string
    return " ".join(strArr)


def binaryStringToString(binString):
    """
    given a string of bytes, return its character equivalent 

    Args:
        binString (str): binary string

    Returns:
        str: character string w/ bytes converted to chars
    """
    return intArrayToString(binaryStringToIntArray(binString))


def stringToBinaryString(string):
    """
    given a string of characters, return its binary equivalent 

    Args:
        string (str): character string

    Returns:
        str: binary string w/ chars converted to bytes
    """
    # given a string of chars, return a binary string
    return intArrayToBinaryString(stringToIntArray(string))


def matchLength(string, length):
    """
    returns string edited so it reaches len length

    Args:
        string (str): original string
        length (int): new length of string

    Returns:
        str: string based on original string with len length
    """

    # if shorter than length then elongate it
    if (len(string) < length):
        return elongate(string, length)

    # else return first length chars in string
    return string[0:length]


def elongate(string, length):
    """
    elongates string into a new string of len length

    Args:
        string (str): original string
        length (int): new length of string

    Returns:
        str: string based on original string with len length
    """
    # returns 'string' concatted with itself until it reaches len length

    numConcats = length // len(string)
    newString = string * numConcats

    # add remainder
    numAddedLetters = length - (len(string) * numConcats)
    newString += string[0:numAddedLetters]

    return newString


def addToNoRemainder(intArr, toAdd, length):
    """
    adds int toAdd to end of intArr until len(intArr) divides length w/ no remainder

    Args:
        intArr (int array): int array to elongate
        toAdd (int): int to add to the end of intArr
        length (int): number that the end length of intArr should divide (not zero)

    Returns:
        int arr: that contains all of intArr and as many additional ints "toAdd" to make it 
        so that it divides evenly into blocks of len length
    """
    if (len(intArr) % length != 0):
        num = length - (len(intArr) % length)

        return (intArr + [toAdd] * num)
    return intArr


def toIntArray(string, binary):
    """
    converts a string (binary or character) into an int array

    Args:
        string (str): string (binary or character)
        binary (bool): true if string is a binary string, false if char array

    Returns:
        int array: int array based on string
    """
    # converts a string (binary or reg) to an int array
    if binary:
        return binaryStringToIntArray(string)
    return stringToIntArray(string)


def stringSplit(string, n, binary=False):
    """
    splits string into n equal substrings - elongates string if not possible

    Args:
        string (str): original string (binary or character)
        n (int): number of substrings to split it into 
        binary (bool, optional): true if string is a binary string. Defaults to False.

    Returns:
        str array: str array based on string with n elements in it
    """
    # remove spaces if binary
    if binary:
        string = str.replace(string, ' ', '')

    # if not divisible by n, elongate so it is
    remainder = len(string) % n
    if remainder != 0:
        string = elongate(string, len(string) + (n - remainder))

    # split up into n parts
    chunk = int(len(string)/n)
    string = [string[i*chunk: (i+1)*chunk] for i in range(n)]

    return string


def removeEnding(arr, val):
    """returns arr that does not end with val (removes instances of val at the end)

    Args:
        arr (int array)
        val (int): int to remove at the end of arr

    Returns:
        int array that doesn't end with val 
    """

    i = len(arr)
    while (i - 1) >= 0 and (arr[i-1] == val):
        i -= 1

    return arr[:i]


def unpack(arr):
    """unpacks nested list/array

    Args:
        arr (array): nested array

    Returns:
        array: array with all elements in it not nested
    """
    return unpackRecurse(arr, [])


def unpackRecurse(nested, all):
    for sub in nested:
        if isinstance(sub, list):
            all = unpackRecurse(sub, all)
        else:
            all += [sub]

    return all


def addModular(arr, toAdd):
    """adds 1 to int array as if it were a binary number (i.e. keeping each element in the array within the 
    range [0, mod] utilizing modular addition). 

    Args:
        arr (int array)

    Returns:
        newArr (int array)
    """
    # convert to binary string then to number
    binString = intArrayToBinaryString(arr)
    binNum = binaryStringToInt(binString)
    maxNum = 2**(len(arr) * 8)
    binNum = (binNum + toAdd) % maxNum

    # reconvert into int array
    binNum = intToBinaryString(binNum)
    newArr = binaryStringToIntArray(binNum)

    # ensure new int array is same size as old one
    if (len(newArr) < len(arr)):
        addZeros = len(arr) - len(newArr)
        newArr = [0] * addZeros + newArr

    return newArr


def prepareBC(txt, key, binTxt, binKey, blen):
    # prepares text, key, and number of blocks for use in block cipher scheme

    txt = toIntArray(txt, binTxt)
    key = toIntArray(key, binKey)

    # split txt into into n blocks of length blen
    # if m has indivisible length to blen, add spaces to the end
    txt = addToNoRemainder(txt, ord(" "), blen)
    blocks = len(txt)//blen
    txt = stringSplit(txt, blocks)

    return (txt, key, blocks)


def PRG(seedArr):
    """
    length-doubling pseudo-random generator
    can't be proven secure without proving P=NP
    indistinguishable from random given that the seed is uniform and not used for anything else

    Args:
        seedArr (int array): int array of length n

    Returns:
        int array: pseudo-random int array of length 2n
    """

    # deterministic, uses same values for same input
    length = len(seedArr)
    halfLength = length//2
    coeff1 = sum(seedArr[0:halfLength]) - seedArr[0]
    coeff2 = sum(seedArr[halfLength:]) + seedArr[-1]
    # add a number after multiplying so not all odd/even elements are divisible by a given coefficient
    added = seedArr[0] + seedArr[halfLength] + seedArr[-1]

    # given two deterministically found coefficients, multiply each int in the arr by a coefficient
    # and add another value to it before modding 256 (so it's still ascii) and combine into new array
    # combine in a zipper, so an int in position k will have been multiplied by coeff1,
    # one in position k+1 will have been multiplied by coeff2

    newArr = [0] * 2 * length
    for i in range(length):
        newArr[2*i] = (coeff1 * (seedArr[i]) + added + i**2) % 256
        newArr[2*i + 1] = (coeff2 * (seedArr[i]) + added + (i+1)**2) % 256

    return newArr


def altPRF(k, x, binK=False, binX=False):
    """
    pseudo-random function composed of PRGs - secure if PRG is secure
    computationally intensive!!
    traverses through a binary tree of height n

    Args:
        k (_type_): string (binary or character) of length m
        x (_type_): string (binary or character) of length n
        binK (bool, optional): true if k is a binary string. Defaults to False.
        binX (bool, optional): true if x is a binary string. Defaults to False.

    Returns:
        int array: pseduo-random int array of length m
    """

    # convert k to int array
    kInt = toIntArray(k, binK)

    # convert x to binary string
    if not binX:
        x = stringToBinaryString(x)
    x = x.replace(" ", "")  # remove spaces

    # traverse through binary tree of PRGS
    v = kInt
    half = len(v)
    for chr in x:
        total = PRG(v)
        # if next char in x is a 0 go left, if is 1 go right
        if chr == "0":
            v = total[:half]
        else:
            v = total[half:]

    return v


def PRF(k, x):
    """
    pseudo-random function 
    impossible to prove secure without proving P=NP, can possibly prove insecure

    Args:
        k (int array): key as int array
        x (int array): int array of length n

    Returns:
        int array: pseduo-random int array of length n
    """
    # pseudo-random function
    # k by x -> v (length of x)
    # k, x, v are int arrays

    # frequently re-used values
    sumX = sum(x)
    sumK = sum(k)
    lenK = len(k)
    c = sumX + sumK + x[len(x)//2] + k[lenK//2]

    v = [0] * len(x)
    for i in range(len(v)):
        add = k[-(i % lenK)] + x[-i] + i**2

        v[i] = ((c + i)*k[i % lenK] + add) % 256

    return v


def PRP(k, v):
    """
    4-round fiestel cipher PRP (invertible PRF)
    based on PRF - secure if PRF is secure

    Args:
        k (int array): key int array
        v (int array): plaintext int array of length n 

    Returns:
        int array that represents ciphertext - length n 
    """
    # split k into 4, v into 2
    k = stringSplit(k, 4)
    v = stringSplit(v, 2)

    # fiestel rounds
    for i in range(4):
        newV = XOR(PRF(k[i], v[1]), v[0])
        v[0] = v[1]
        v[1] = newV

    return v[0] + v[1]


def PRPinv(k, v):
    """
    4-round inverse fiestel cipher PRP (invertible PRF)

    Args:
        k (int array): int array of key
        v (int array): int array of ciphertext (length n)

    Returns:
        int array of length n that represents plaintext
    """
    # split k into 4, v into 2
    k = stringSplit(k, 4)
    v = stringSplit(v, 2)

    # fiestel rounds
    for i in range(3, -1, -1):
        # newV = XOR(PRF(k[i], intArrayToString(v[0])), v[1])
        newV = XOR(PRF(k[i], v[0]), v[1])
        v[1] = v[0]
        v[0] = newV

    return v[0] + v[1]


def invalidRSAPrimes(p, q):
    return (p == None) or (q == None) or (p == q) or (not isPrime(p)) or (not isPrime(q))


def isPrime(n):
    """returns true if n is prime, else returns false

    Args:
        n (int): a prime(?) number
    """

    if n <= 1:
        return False

    i = 2
    top = n//i
    # test if divisible -
    # only need to test up to n//i bc anything above would be divisible by something less than i
    while (i < top + 1):
        if (n % i == 0):
            return False
        i += 1
        top = n//i

    return True


def getPrime(min, max):
    """generates a prime number in the range [2, max]

    Args:
        max (int): maximum number that the prime could be
    """
    # if too small a number, return 1
    if (max <= 2 or max <= min):
        return 1

    loop = 0
    while (loop < 20):
        # generate a random number in the range, find smallest prime between n and max
        # if no primes from n to max, generate new n and try again
        n = random.randint(min, max)
        while (n <= max):
            if (isPrime(n)):
                return n
            # only increase by odds since only even prime is 2
            if (n % 2 == 0):
                n += 1
            else:
                n += 2
        loop += 1

    # if haven't found after 20 loops, just return 1
    return 1


def getCoPrime(n):
    """return a number m < n such that gcd(n, m) = 1

    Args:
        n (int): int to generate a coprime int for
    """
    # if too small a number, return 1
    if (max <= 3):
        return 1

    loop = 0
    while (loop < 20):
        # generate a random number in the range, find smallest coprime val between m and n
        # if no coprime vals from m to n, generate new m and try again
        m = random.randint(2, max)
        while (m < n):
            if (gcd(m, n) == 1):
                return m
            m += 1
        loop += 1

    # if haven't found after 20 loops, just return 1
    return 1


def gcd(m, n):
    res = min(m, n)

    while res > 0:
        if m % res == 0 and n % res == 0:
            break
        res -= 1

    return res


def getMultInverse(a, n):
    """return b such that (a * b % n) = 1

    Args:
        a (int): element to find inverse for
        n (int): mod
    """

    for b in range(1, n):
        if (a * b) % n == 1:
            return b

    return -1


def modExp(x, e, N):
    """returns x^e % N, less computationally intensive. from mike rosulek's "The Joy of Cryptography".

    Args:
        x (int): value to be exponentiated
        e (int): exponent
        N (int): modular value        
    """

    if e == 0:
        return 1
    # if even
    if (e % 2 == 0):
        return (modExp(x, e/2, N)**2) % N
    # else is odd
    return (modExp(x, (e-1)/2, N)**2 * x) % N

# pylint: disable=invalid-name
# utility functions
import re  # regex


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


def intArrayToBinaryString(arr):
    # given an int array, convert each int into binary and then return a string of all bytes separated by spaces
    strArr = [bin(i)[2:].zfill(8) for i in arr]
    # zfill 8 so it keeps leading zeros, [2:] so it doesnt put '0b' prefix into string
    return " ".join(strArr)


def binaryStringToString(binString):
    # given a binary string, return it as a string w/ bytes converted to chars
    return intArrayToString(binaryStringToIntArray(binString))


def stringToBinaryString(string):
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
        string = elongate(string, len(string) + remainder)

    # split up into n parts
    chunk = int(len(string)/n)
    string = [string[i*chunk: (i+1)*chunk] for i in range(n)]

    return string


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


def PRF(k, x, binK=False, binX=False):
    """
    pseudo-random function 
    impossible to prove secure without proving P=NP, can possibly prove insecure

    Args:
        k (_type_): string (binary or character) 
        x (_type_): string (binary or character) of length n
        binK (bool, optional): true if k is a binary string. Defaults to False.
        binX (bool, optional): true if x is a binary string. Defaults to False.

    Returns:
        int array: pseduo-random int array of length n
    """
    # pseudo-random function
    # k by x -> v (length of x)
    # k, x are strings (binary or regular)
    # v is an int array

    # convert k and x to int arrays
    arrK = toIntArray(k, binK)
    arrX = toIntArray(x, binX)

    # frequently re-used values
    sumX = sum(arrX)
    sumK = sum(arrK)
    lenK = len(arrK)
    c = sumX + sumK + arrX[len(arrX)//2] + arrK[lenK//2]

    v = [0] * len(arrX)
    for i in range(len(v)):
        add = arrK[-(i % lenK)] + arrX[-i] + i**2

        v[i] = ((c + i)*arrX[i] + add) % 256

    return v


def PRP(k, v, binK=False, binV=False):
    """
    4-round fiestel cipher PRP (invertible PRF)
    based on PRF - secure if PRF is secure

    Args:
        k (string): string (binary or character) of key
        v (string): string (binary or regular) of plaintext - length n 
        binK (bool, optional): true if k is a binary string. Defaults to False.
        binV (bool, optional): true if v is a binary string. Defaults to False.

    Returns:
        string: string (of same type as v) that represents ciphertext - length n 
    """
    # split k into 4, v into 2
    k = stringSplit(k, 4, binK)
    v = stringSplit(v, 2, binV)

    # convert v substrings to int arrays
    v = [toIntArray(substr, binV) for substr in v]

    # fiestel rounds
    for i in range(4):
        newV = XOR(PRF(k[i], intArrayToString(v[1])), v[0])
        v[0] = v[1]
        v[1] = newV

    if binV:
        v = [intArrayToBinaryString(i) for i in v]
        v[0] += " "  # add a space between bytes
    else:
        v = [intArrayToString(i) for i in v]

    return v[0] + v[1]


def PRPinv(k, v, binK=False, binV=False):
    """
    4-round inverse fiestel cipher PRP (invertible PRF)

    Args:
        k (string): string (binary or character) of key
        v (string): string (binary or regular) of ciphertext.
        binK (bool, optional): true if k is a binary string. Defaults to False.
        binV (bool, optional): true if v is a binary string. Defaults to False.

    Returns:
        string: string (of same type as v) that represents plaintext
    """
    # split k into 4, v into 2
    k = stringSplit(k, 4, binK)
    v = stringSplit(v, 2, binV)

    # convert v substrings to int arrays
    v = [toIntArray(substr, binV) for substr in v]

    # fiestel rounds
    for i in range(3, -1, -1):
        newV = XOR(PRF(k[i], intArrayToString(v[0])), v[1])
        v[1] = v[0]
        v[0] = newV

    if binV:
        v = [intArrayToBinaryString(i) for i in v]
        v[0] += " "  # add a space between bytes
    else:
        v = [intArrayToString(i) for i in v]

    return v[0] + v[1]

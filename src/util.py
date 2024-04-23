# utility functions
import re  # regex


def stringToIntArray(string):
    # make a string into an integer array - each element is the int representation of the character in that index

    # ord(character) transforms a char to the int that it represents in ascii
    return [ord(c) for c in string]


def intArrayToString(arr):
    # makes an int array into a string - each int will be an ascii char
    return "".join([chr(i) for i in arr])


def splitBinaryToBytes(binString):
    # split a string of 0's and 1's into a string array split by byte

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

    binString = splitBinaryToBytes(binString)
    return [int(binByte, 2) for binByte in binString]


def intArrayToBinaryString(arr):
    # given an int array, convert each int into binary and then return a string of all bytes separated by spaces
    strArr = [bin(i)[2:].zfill(8) for i in arr]
    # zfill 8 so it keeps leading zeros, [2:] so it doesnt put '0b' prefix into string
    return " ".join(strArr)


def binaryStringToString(binString):
    # given a binary string, return it as a string w/ bytes converted to chars

    binString = splitBinaryToBytes(binString)
    charArray = [chr(int(i, 2)) for i in binString]

    return "".join(charArray)


def matchLength(string, length):
    # returns new string with len length

    # if shorter than length then elongate it
    if (len(string) < length):
        return elongate(string, length)

    # else return first length chars in string
    return string[0:length]


def elongate(string, length):
    # returns 'string' concatted with itself until it reaches len length

    numConcats = length // len(string)
    newString = string * numConcats

    # add remainder
    numAddedLetters = length - (len(string) * numConcats)
    newString += string[0:numAddedLetters]

    return newString


def PRG(seedArr):
    # length doubling psuedo-random generator
    # takes an int arr of length n and returns a psuedorandom int arr of length 2n
    # indistinguishable from random given that seed is uniform and not used for anything else
    # can't be proven to be secure without proving P = NP

    # deterministic, uses same values for same input
    length = len(seedArr)
    halfLength = length//2
    coeff1 = sum(seedArr[0:halfLength])
    coeff2 = sum(seedArr[halfLength:])
    # add a number after multiplying so not all odd/even elements are divisible by a given coefficient
    added = seedArr[halfLength]

    # given two deterministically found coefficients, multiply each int in the arr by a coefficient
    # and add another value to it before modding 256 (so it's still ascii) and combine into new array
    # combine in a zipper, so an int in position k will have been multiplied by coeff1,
    # one in position k+1 will have been multiplied by coeff2

    newArr = [0] * 2 * length
    for i in range(2*length):
        if (i % 2 == 0):
            newArr[i] = (coeff1 * (seedArr[i//2]) + added) % 256
        else:
            newArr[i] = (coeff2 * seedArr[i//2] + added) % 256

    return newArr

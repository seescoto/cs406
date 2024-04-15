# utility functions
import re  # regex


def stringToIntArray(string):
    # make a string into an integer array - each element is the int representation of the character in that index

    # ord(character) transforms a char to the int that it represents in ascii
    return [ord(c) for c in string]


def intArrayToString(arr):
    # makes an int array into a string - each int will be an ascii char
    return "".join([chr(i) for i in arr])


def binaryStringToIntArray(binString):
    # given a string of 0's and 1's (as characters)
    # convert it to an int array where each 'byte' becomes an integer in the array

    if (re.findall(r'\s+', binString)):
        # if contains whitespace, split by whitespace
        binString = binString.split()
    else:
        # else split so each binByte has 8 chars in it
        binString = [binString[i:i+8] for i in range(0, len(binString), 8)]

    return [int(binByte, 2) for binByte in binString]


def intArrayToBinaryString(arr):
    # given an int array, convert each int into binary and then return a string of all bytes separated by spaces
    strArr = [bin(i)[2:].zfill(8) for i in arr]
    # zfill 8 so it keeps leading zeros, [2:] so it doesnt put '0b' prefix into string
    return " ".join(strArr)


def binaryStringToString(binString):
    binString = binString.split(" ")
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

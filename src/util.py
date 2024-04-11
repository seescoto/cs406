# utility functions

def stringToIntArray(string):
    # make a string into an integer array - each element is the int representation of the character in that index

    # ord(character) transforms a char to the int that it represents in ascii
    return [ord(c) for c in string]


def intArrayToString(arr):
    # makes an int array into a string - each int will be an ascii char
    return "".join([chr(i) for i in arr])


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

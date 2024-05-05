import random 

def genRandomIntArray(n):
    # generates a random array of n integers 0 - 255
    return [random.randint(0, 255) for _ in range(n)]

def genRandomString(n):
    # generates a random string of n chars 
    #ascii values 32 - 126 are printable chars 
    return "".join([chr(random.randint(32, 126)) for _ in range(n)])
     

def runningAvg(val, n, prevAvg=0):
    # welford's algorithm for computing running average without storing any values or sum
    # https://en.wikipedia.org/wiki/Algorithms_for_calculating_variance#Welford's_online_algorithm
    return (prevAvg + (val - prevAvg)/n)


def getRange(arr):
    # returns range of values in arr
    low = arr[0]
    high = arr[0]
    for i in arr:
        low = min(low, i)
        high = max(high, i)
    return high - low


def getAvg(arr):
    # returns avg of values in arr
    return (sum(arr)/len(arr))

def countEvensOdds(arr):
    #returns number of even and odd nums in arr
    evens = 0 
    for i in arr:
        if i % 2 == 0: 
            evens += 1 

    return (evens, len(arr) - evens)

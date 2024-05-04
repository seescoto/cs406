# testing that PRG in util is (relatively) indistinguishable from random (using random package)
from src import util
import randomFunctions as rf

def test(tests, arrLength):
    meanPRG = 0
    meanRand = 0
    rangePRG = 0
    rangeRand = 0
    for i in range(1, tests+1):
        # random array of length arrLength
        randArr = rf.genRandomIntArray(arrLength)
        meanRand = rf.runningAvg(rf.getAvg(randArr), i, meanRand)
        rangeRand = rf.runningAvg(rf.getRange(randArr), i, rangeRand)

        # array of length arrLength generated by prg in util
        prgArr = util.PRG(rf.genRandomIntArray(arrLength//2))
        meanPRG = rf.runningAvg(rf.getAvg(prgArr), i, meanPRG)
        rangePRG = rf.runningAvg(rf.getRange(prgArr), i, rangePRG)

    print("mean of PRG generated array: \t\t\t" + str(meanPRG))
    print("mean of randomly generated array: \t\t" + str(meanRand))
    print("avg. range of PRG generated array: \t\t" + str(rangePRG))
    print("avg. range of randomly generated array: \t" + str(rangeRand))


if __name__ == '__main__':
    test(50000, 100)

"""
results = 

mean of PRG generated array:                    127.50630580000013
mean of randomly generated array:               127.51785759999946
avg. range of PRG generated array:              250.74767999999867
avg. range of randomly generated array:         250.90437999999855

Summary results are very similar for both randomly generated array using random package (tested PRG) and 
my own prg (non-tested) and look indistinuishable (though range of randomly generated is slightly higher). 
Because no PRG can be proven secure, this seems like a sufficient test of reliability for the randomness 
we can get.
"""

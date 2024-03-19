
from HewiUaprior import HewiUaprior
from WdFim import WdFim
import sys
from File import File



def main():
    expectedWeightedSupport = float(sys.argv[1])
    if expectedWeightedSupport>1 or expectedWeightedSupport <0:
        print('Please enter expected weighted Support between 0-1')
        return
 
    reliableProbabilisticSupport = float(sys.argv[2])
    if reliableProbabilisticSupport>1 or reliableProbabilisticSupport <0:
        print('Please enter ???? between 0-1')
        return

    dataBaseWdFim,fileNameWdFim = File().createDataBase('WdFim')
    WdFim().execute(dataBaseWdFim,expectedWeightedSupport,reliableProbabilisticSupport,fileNameWdFim)
    dataBaseHewi,fileNameHewi = File().createDataBase('Hewi')
    HewiUaprior().execute(dataBaseHewi,expectedWeightedSupport,reliableProbabilisticSupport,fileNameHewi)



    # T40I10D100K = File().readFile('input/DataTest/T40I10D100K.txt','input/DataTest/T40I10D100K-weight-table.txt')
    # mushroom = File.readFile('input/DataTest/mushroom.txt','input/DataTest/mushroom-weight-table.txt')
    # retail = File().readFile('input/DataTest/retail.txt','input/DataTest/retail-weight-table.txt')




    # WdFim().execute(mushroom,expectedWeightedSupport,reliableProbabilisticSupport,'mushroom-' + str(expectedWeightedSupport * 100)+'%-test.txt')
    # WdFim().execute(retail,expectedWeightedSupport,reliableProbabilisticSupport,'retail-' + str(expectedWeightedSupport * 100)+'%.txt')
    # WdFim().execute(T40I10D100K,expectedWeightedSupport,reliableProbabilisticSupport,'T40I10D100K-' + str(expectedWeightedSupport * 100)+'%.txt')

    # HewiUaprior().execute(mushroom,expectedWeightedSupport,reliableProbabilisticSupport,'mushroom-' + str(expectedWeightedSupport * 100)+'%-test.txt')
    # HewiUaprior().execute(retail,expectedWeightedSupport,reliableProbabilisticSupport,'retail-' + str(expectedWeightedSupport * 100)+'%.txt')
    # HewiUaprior().execute(T40I10D100K,expectedWeightedSupport,reliableProbabilisticSupport,'T40I10D100K-' + str(expectedWeightedSupport * 100)+'%.txt')

if __name__ == "__main__":
    main()

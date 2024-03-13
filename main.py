
from HewiUaprior import HewiUaprior
from WdFim import WdFim

from File import File



def main():
    value = 0.01

    dataBaseWdFim,fileNameWdFim = File().createDataBase('WdFim')
    WdFim().execute(dataBaseWdFim,value,fileNameWdFim)
    dataBaseHewi,fileNameHewi = File().createDataBase('Hewi')
    HewiUaprior().execute(dataBaseHewi,value,fileNameHewi)



    # T40I10D100K = File().readFile('input/DataTest/T40I10D100K.txt','input/DataTest/T40I10D100K-weight-table.txt')
    # mushroom = File.readFile('input/DataTest/mushroom.txt','input/DataTest/mushroom-weight-table.txt')
    # retail = File().readFile('input/DataTest/retail.txt','input/DataTest/retail-weight-table.txt')




    # WdFim().execute(mushroom,value,'mushroom-' + str(value * 100)+'%-test.txt')
    # WdFim().execute(retail,value,'retail-' + str(value * 100)+'%.txt')
    # WdFim().execute(T40I10D100K,value,'T40I10D100K-' + str(value * 100)+'%.txt')

    # HewiUaprior().execute(mushroom,value,'mushroom-' + str(value * 100)+'%-test.txt')
    # HewiUaprior().execute(retail,value,'retail-' + str(value * 100)+'%.txt')
    # HewiUaprior().execute(T40I10D100K,value,'T40I10D100K-' + str(value * 100)+'%.txt')

if __name__ == "__main__":
    main()

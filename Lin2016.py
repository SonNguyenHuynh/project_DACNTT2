
import os
from Apriori import apriori
from ItemDto import ItemDto
from ItemsetWeightCalculator import itemsetWeightCalculator
from TidDto import TidDto
from TransactionDTO import TransactionDTO
from WeightTable import WeightTable
from DS import DS
from ExpectedSupportCalculator import  expectedSupportCalculator
from ExpectedWeightedSupportCalculator import expectedWeightedSupport
from Util import getItemByLength, powerset
from Util import AprioriGen
import random
from collections import defaultdict

from calculatoritemsetProbabilityInATransaction import calculatorItemsetProbabilityInATransaction



class Lin2016:
    
    def execute(self):    
        # weight_table = WeightTable()
        dataBase = Lin2016().createDataBase()
        # dataBase = Lin2016().readFile()

        transactions = dataBase[0]
        weightTable = dataBase[1]
        # weightOfSyntheticChain = weightTable.calculate_probability()
        # print(weightOfSyntheticChain)



        
        # print(weightOfSyntheticChain)
        ds = DS(tid=1, transactions=transactions)
        # syntheticChain = ds.syntheticChain
        expectedWeighted = 0.1
        expectedWeightedValue = len(ds.transactions) * expectedWeighted
        
        data=[]
        for i in ds.transactions:
            tidKeys=[]
            for j in i.items:
                tidKeys.append(j.item)
            data.append(set(tidKeys))
            # data.append(set(item for item in i.items)) 

        tubw =[]
        tubp = []
        tubwp= []

        for i in ds.transactions:
            tubw=i.calculateTubw(weightTable)
            tubp=i.calculateTubp()
            tubwp.append(tubw.probability*tubp.probability)



        # print('tubw : ')
        # print(tubw)

        # print('tubp')
        # print(tubp)

        # print('tubwp')
        # tubwp = Lin2016().calculatetTubwp(tubp,tubw)
        # print(tubwp)

        # print('iubwp')
        iubwp= Lin2016().calculatetIubwp(ds,tubwp)
        # print(iubwp)

        HUBEWIs =[]
        currentLSet=[]
        HEWIs=[]
        for i in iubwp:
            if(i.probability>=expectedWeightedValue):
                currentLSet.append(frozenset({i.item}))
                HUBEWIs.append(i)
        
        k=2
        globalItemSetWithSup = defaultdict(int)

        while(len(currentLSet)):

            ck= apriori(currentLSet,data,0.3,0.5,k,globalItemSetWithSup)
            globalItemSetWithSup=ck[2]
            HUBEWIk=[]
            for i in ck[0]:
                iubwp= Lin2016().calculatetIubwpWithCk(i,ds,tubwp)

                if(iubwp.probability >=expectedWeightedValue):
                    HUBEWIk.append(frozenset(iubwp.item))
                    HUBEWIs.append(iubwp)
            currentLSet=[]
            currentLSet=HUBEWIk
            k=k+1
        


        # Calculate Expected Support of an Itemset
        for i in HUBEWIs:
            itemsetProbabilityInATransaction= calculatorItemsetProbabilityInATransaction(i,ds)
            expectedSupportValue = expectedSupportCalculator(i, itemsetProbabilityInATransaction)
            # print(f"Expected Support of : {expectedSupportValue}")
            # print(expectedSupportValue)
        
            
            itemsetWeight = itemsetWeightCalculator(expectedSupportValue,weightTable)
            print(itemsetWeight)

            # # Calculate Expected Weighted Support of an Itemset
            expectedWeightedSupportValue = expectedWeightedSupport(itemsetWeight, expectedSupportValue)
            # # print(f"Expected Weighted Support")
            print(expectedWeightedSupportValue)

            if(expectedWeightedSupportValue.probability >=expectedWeightedValue ):
                HEWIs.append(expectedWeightedSupportValue)
        
        for i in HEWIs:
            print(i.item,i.probability)
        Lin2016().writeFile(HEWIs)
        
        print('done')

    def writeFile(self,data:[ItemDto]):
        folder_path = "output"
        file_path = "example.txt"


        # Ensure the folder exists, create it if necessary
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Construct the full file path
        file_path = os.path.join(folder_path, file_path)


        with open(file_path, 'w') as file:
            for i in data:
                file.write(str(set(i.item)) +' : '+ str(i.probability) + '\n')


    def calculatorHewis(self,expectedWeightedSupportValue: list[ItemDto],expectedWeightedValue:int):
        result =[]
        for i in expectedWeightedSupportValue:
            if(i.probability >=expectedWeightedValue):
                result.append(i)

        return result

    def calculatorHubewi(self,iubwp,expectedWeightedValue):
        result =[]
        for i in iubwp:
            if(i.get(list(i.keys())[0])>=expectedWeightedValue):
                result.append(i)
        sortedData = sorted(result, key=lambda x: len(list(x.keys())[0]))

        return sortedData




    def calculatorTubwp(self,tubp,tubw):
        result =[]
        for i in tubp:
            for j in tubw:
                if(list(i.keys())[0] == list(j.keys())[0]):
                    tubpValue =  i.get(list(i.keys())[0])
                    tubwValue = j.get(list(j.keys())[0])
                    tubwpValue = tubpValue * tubwValue
                    
                    result.append({list(i.keys())[0]:tubwpValue})
        return result

    def calculatetIubwp(self,ds:DS,tubwp):
        iubwp = []
        for i in ds.transactions:
            for j in i.items:
                if(len(iubwp)==0):
                    tubwpValue =tubwp[i.tid-1]
                    iubwp.append(ItemDto(item=j.item,probability=tubwpValue))
                else:
                    checkValue= False
                    for k in iubwp:
                        if(k.item == j.item):
                            checkValue =True
                            break
                    if(checkValue):
                        tubwpValue =tubwp[i.tid-1]
                        k.probability = k.probability + tubwpValue
                    else:
                        tubwpValue =tubwp[i.tid-1]
                        iubwp.append(ItemDto(item=j.item,probability=tubwpValue))
        return iubwp
    
    def calculatetIubwpWithCk(self,itemck:set,ds:DS,tubwp):
        total = 0
        for transaction in ds.transactions:
            count = 0 
            for item in transaction.items:
                for i in itemck:
                    if(item.item == i):
                        count+=1
            if(count == len(itemck)):
                total+=tubwp[transaction.tid -1]
        return ItemDto(item=itemck,probability=total)

    
    
    
    
    
    def createDataBase(self):
        # transaction1 = TransactionDTO(item=[ItemDto(item='A',probability=0.25),ItemDto(item='C',probability=0.4),ItemDto(item='E',probability=1.0)])
        # transaction2 = TransactionDTO(item=[ItemDto(item='D',probability=0.35),ItemDto(item='F',probability=0.7)])
        # transaction3 = TransactionDTO(item=[ItemDto(item='A',probability=0.7),ItemDto(item='B',probability=0.82),ItemDto(item='C',probability=0.9),ItemDto(item='E',probability=1.0),ItemDto(item='F',probability=0.7)])
        # transaction4 = TransactionDTO(item=[ItemDto(item='D',probability=1.0),ItemDto(item='F',probability=0.5)])
        # transaction5 = TransactionDTO(item=[ItemDto(item='B',probability=0.4),ItemDto(item='C',probability=0.4),ItemDto(item='D',probability=1.0)])
        # transaction6 = TransactionDTO(item=[ItemDto(item='A',probability=0.8),ItemDto(item='B',probability=0.8),ItemDto(item='C',probability=1.0),ItemDto(item='F',probability=0.3)])
        # transaction7 = TransactionDTO(item=[ItemDto(item='B',probability=0.8),ItemDto(item='C',probability=0.9),ItemDto(item='D',probability=0.5),ItemDto(item='E',probability=1.0)])
        # transaction8 = TransactionDTO(item=[ItemDto(item='B',probability=0.65),ItemDto(item='B',probability=0.8)])
        # transaction9 = TransactionDTO(item=[ItemDto(item='B',probability=0.5),ItemDto(item='D',probability=0.8),ItemDto(item='F',probability=1.0)])
        # transaction10 = TransactionDTO(item=[ItemDto(item='A',probability=0.4),ItemDto(item='B',probability=1.0),ItemDto(item='C',probability=0.9),ItemDto(item='E',probability=0.85)])
        
        weightTable = WeightTable({'A': 0.2, 'B': 0.75, 'C': 0.9, 'D': 1.0, 'E': 0.55, 'F': 0.3})

        transactions_data = [
            [('A', 0.25), ('C', 0.4), ('E', 1.0)],
            [('D', 0.35), ('F', 0.7)],
            [('A', 0.7), ('B', 0.82), ('C', 0.9), ('E', 1.0),('F',0.7)],
            [('D', 1.0), ('F', 0.5)],
            [('B', 0.4), ('C', 0.4), ('D', 1.0)],
            [('A', 0.8), ('B', 0.8), ('C', 1.0), ('F', 0.3)],
            [('B', 0.8), ('C', 0.9), ('D', 0.5), ('E', 1.0)],
            [('B', 0.65), ('E', 0.4)],
            [('B', 0.5), ('D', 0.8), ('F', 1.0)],
            [('A', 0.4), ('B', 1.0), ('C', 0.9), ('E', 0.85)],
        ]

        transactions = [
            TransactionDTO(tid=i+1, items=data, weight_table=weightTable) for i, data in enumerate(transactions_data)
        ]

        return [transactions,weightTable]
    
    def readFile(self):
        data=[]
        items=[]
        with open('data.txt', 'r') as file:
            for line in file:
                itemList = line.split()
                dataLine = [int(number) for number in itemList]
                data.append(dataLine)

                for item in itemList:
                    dataLine=[item]
                    items.append(str(item))
        items = sorted(list(set(items)))

        # print(data)
        # print(items)
        convertItems  = {key: round(random.uniform(0, 1), 2) for key in items}
        # print(convertItems)
        convertData = [[(str(item), round(random.uniform(0, 1), 2)) for item in sublist] for sublist in data]
        # print(convertData)

        weightTable = WeightTable(convertItems)
        transactions_data = convertData
        transactions = [
            TransactionDTO(tid=i+1, items=data, weight_table=weightTable) for i, data in enumerate(transactions_data)
        ]

        return [transactions,weightTable]
    







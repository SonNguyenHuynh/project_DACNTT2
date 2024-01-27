
import WdFim
import os
from collections import defaultdict
from multiprocessing import process
import time

import psutil
from Apriori import apriori
from ExpectedSupportCalculator import expectedSupportCalculator, expectedSupportCalculatorWithFrozenset
from ItemDto import ItemDto
from ItemsetSupportCalculators import itemsetWeight
from ItemsetWeightCalculator import itemsetWeightCalculator
from TidDto import TidDto
from TransactionDTO import TransactionDTO
from WeightTable import WeightTable
from DS import DS
from ExpectedWeightedSupportCalculator import expectedWeightedSupport
from itertools import product
from calculatoritemsetProbabilityInATransaction import calculatorItemsetProbabilityInATransactionWithFrozenset




class WdFim:

    def execute(self):    
    # weight_table = WeightTable()
        dataBase,fileName = WdFim().createDataBase()
        WdFim().handleLogic(dataBase,0.1,fileName)
        value = 0.01

        mushroom = WdFim().readFile('input/DataTest/mushroom.txt','input/DataTest/mushroom-weight-table.txt')
        WdFim().handleLogic(mushroom,value,'mushroom-' + str(value * 100)+'%-test.txt')
        retail = WdFim().readFile('input/DataTest/retail.txt','input/DataTest/retail-weight-table.txt')
        WdFim().handleLogic(retail,value,'retail-' + str(value * 100)+'%.txt')
        T40I10D100K = WdFim().readFile('input/DataTest/T40I10D100K.txt','input/DataTest/T40I10D100K-weight-table.txt')
        WdFim().handleLogic(T40I10D100K,value,'T40I10D100K-' + str(value * 100)+'%.txt')
    
    def handleLogic(self,dataBase: list,minEWSup: int,filename:str):    
        print('start')
        process = psutil.Process()

        startTime = time.time()
        startMemory = process.memory_info().rss / (1024 ** 2)  # in megabytes
        # weight_table = WeightTable()
        transactions = dataBase[0]
        weightTable = dataBase[1]
        
        # print(weightOfSyntheticChain)
        ds = DS(tid=1, transactions=transactions)
        expectedWeighted = minEWSup
        expectedWeightedValue = len(ds.transactions) * expectedWeighted
        data=[]
        for i in ds.transactions:
            tidKeys=[]
            for j in i.items:
                tidKeys.append(j.item)
            data.append(set(tidKeys))
            # data.append(set(item for item in i.items)) 
        
        WFIS,CWFIS1= WdFim().calculateExpwSup(ds=ds,weightTable=weightTable,expectedWeightedValue=expectedWeightedValue)

        WFISK_1=WFIS

        SCWFIS1 = CWFIS1
        CWFISK_1 = CWFIS1

 
        SCWFIS1.sort(key=lambda x: x.probability)

        k=2

        while(len(WFISK_1)):
            # tinh to hop k
            CWFISK  = WdFim().connection(WFISK_1,CWFIS1,k)

            # NCWFISk = wConnection((CWFISk-1 - WFISk-1), SCWFIS1) 
            removeItem= WdFim().removeItem(CWFISK_1,WFISK_1)
            # tạo tổ hợp B với item trong scwfi1 có popariti nhỏ hơn
            NCWFISK = WdFim().wConnection(removeItem,SCWFIS1,k)
            CWFISK_1 = []

            RCWFISK = WdFim().calculatorRCWFISK(data1=CWFISK,data2=NCWFISK)
            # print(rcwfisk)

            WFISK_1=[]
            for i in RCWFISK:
                itemsetProbabilityInATransaction= calculatorItemsetProbabilityInATransactionWithFrozenset(i,ds)
                expectedSupportValue = expectedSupportCalculatorWithFrozenset(i, itemsetProbabilityInATransaction)
                # print(f"Expected Support of : {expectedSupportValue}")
                # print(expectedSupportValue)
            
                
                itemsetWeight = itemsetWeightCalculator(expectedSupportValue,weightTable)

                # # Calculate Expected Weighted Support of an Itemset
                expectedWeightedSupportValue = expectedWeightedSupport(itemsetWeight, expectedSupportValue)
                # # print(f"Expected Weighted Support")
                CWFISK_1.append(expectedWeightedSupportValue)
                if(expectedWeightedSupportValue.probability >=expectedWeightedValue ):
                    WFIS.append(expectedWeightedSupportValue)  
                    WFISK_1.append(expectedWeightedSupportValue)
            k+=1


        
        endMemory = process.memory_info().rss / (1024 ** 2)  # in megabytes
        memory_usage = endMemory - startMemory

        endTime = time.time()
        runtime = endTime - startTime
        

        WdFim().writeFile(filename,WFIS,runtime,memory_usage,len(ds.transactions),expectedWeighted)
        
        print('done')    
    def calculatorRCWFISK(self,data1:list[frozenset],data2: list[frozenset]):
        RCWFISK:list[frozenset]=[]
        for i in data1:
            isValid =False
            for j in data2:
                if(i == j):
                    isValid =True
            if(isValid == False):
                RCWFISK.append(i)  

        return RCWFISK


        
    def removeItem(self,data1:list[ItemDto],data2: list[ItemDto]):
        result: list[ItemDto] = []
        for i  in data1:
            isValid = False
            for j in data2:
                if(i.item == j.item):
                    isValid = True
            if(isValid == False):
                result.append(i)
        return result



    def wConnection(self,removeItem:list[ItemDto],scwfi: list[ItemDto],length:int):
        result:list[ItemDto] =[]

        for i in removeItem:
            for j in scwfi:
                if(i.probability > j.probability and len(frozenset(i.item).union(frozenset(j.item))) == length):
                    result.append(frozenset(i.item).union(frozenset(j.item)))

        return result
    
    def connection(self,wfis:list[ItemDto],cwfis: list[ItemDto],length:int):
        return set([frozenset(i.item).union(frozenset(j.item)) for i in cwfis for j in wfis if len(frozenset(i.item).union(frozenset(j.item))) == length])
    
    def calculatorWeightItem(self,data:list[frozenset],weightTable: list[ItemDto]):
        result:list[ItemDto] =[]
        for i in data:
            for j in i:
                total=0
                count:[]
                for k in weightTable:
                    if(j==k.item):
                        total+=k.probability
            result.append(ItemDto(item=i,probability=total/len(i)))
        return result



    
    def calculateExpwSup(self,ds:DS,weightTable:WeightTable,expectedWeightedValue:int)-> list[ItemDto]:
        expwSup:list[itemDto] = []
        expSup =[]
        cwfis1:list[ItemDto] = [] 
        for transaction in ds.transactions:
            for itemDto in transaction.items:
                if(len(expSup)==0):
                    weightValue =itemDto.probability
                    expSup.append(ItemDto(item=itemDto.item,probability=weightValue))
                else:
                    checkValue= False
                    for k in expSup:
                        if(k.item == itemDto.item):
                            checkValue =True
                            break
                    if(checkValue):
                        weightValue =itemDto.probability
                        k.probability = k.probability + weightValue
                    else:
                        weightValue =itemDto.probability
                        expSup.append(ItemDto(item=itemDto.item,probability=weightValue))

        for item in expSup:
            probability=item.probability * weightTable.get_weight(item.item)
            cwfis1.append(ItemDto(item=item.item,probability=probability))

            if(probability > expectedWeightedValue):
                expwSup.append(ItemDto(item=item.item,probability=probability))
        return expwSup,cwfis1
    
    def calculateExpwSupWithRcwfis(self,ds:list[frozenset],weightTable:WeightTable,expectedWeightedValue:int)-> list[ItemDto]:
        expwSup = []
        expSup =[]
        for transaction in ds.transactions:
            for itemDto in transaction.items:
                if(len(expSup)==0):
                    weightValue =itemDto.probability
                    expSup.append(ItemDto(item=itemDto.item,probability=weightValue))
                else:
                    checkValue= False
                    for k in expSup:
                        if(k.item == itemDto.item):
                            checkValue =True
                            break
                    if(checkValue):
                        weightValue =itemDto.probability
                        k.probability = k.probability + weightValue
                    else:
                        weightValue =itemDto.probability
                        expSup.append(ItemDto(item=itemDto.item,probability=weightValue))
        for item in expSup:
            probability=item.probability * weightTable.get_weight(item.item)

            if(probability > expectedWeightedValue):
                expwSup.append(ItemDto(item=item.item,probability=probability))
        return expwSup
    
    def createDataBase(self):

        weightTable = WeightTable({'A': 0.1, 'B': 0.8, 'C': 0.3, 'D': 1.0, 'E': 0.6, 'F': 0.1})
        transactions_data = [
            [('A', 0.8), ('B', 0.4), ('D', 1.0)],
            [('B', 0.3), ('F', 0.7)],
            [('B', 0.7), ('C', 0.9), ('E', 1.0), ('F', 0.7)],
            [('E', 1.0), ('F', 0.5)],
            [('A', 0.6), ('C', 0.4), ('D', 1.0)],
            [('A', 0.8), ('B', 0.8), ('C', 1.0), ('F', 0.3)],
            [('A', 0.8), ('C', 0.9), ('D', 0.5), ('E', 1.0)],
            [('C', 0.6), ('E', 0.4)],
            [('A', 0.5), ('D', 0.8), ('F', 1.0)],
            [('A', 0.7), ('B', 1.0), ('C', 0.9), ('E', 0.8)],
        ]

        transactions = [
            TransactionDTO(tid=i+1, items=data, weight_table=weightTable) for i, data in enumerate(transactions_data)
        ]

        return [transactions,weightTable],'example.txt'
    
    def readFile(self,dataFile:str,weightTableFile:str):
        data=[]
        items=[]
        with open(dataFile, 'r') as file:
            for line in file:
                itemList = line.split()
                dataLine = []
                for number in itemList:
                    numberValue = number.strip('()').split(',')
                    dataLine.append((str(numberValue[0]),float(numberValue[1])))
                data.append(dataLine)

        with open(weightTableFile, 'r') as file:
            for line in file:
                itemList = line.split()
                weightTable = {}
                for number in itemList:
                    numberValue = number.strip('()').split(',')
                    weightTable[str(numberValue[0])] = float(numberValue[1])

        # print(data)
        # print(items)
        # convertItems  = {key: round(random.uniform(0, 1), 2) for key in items}
        # print(convertItems)
        # convertData = [[(str(item), round(random.uniform(0, 1), 2)) for item in sublist] for sublist in data]
        # print(convertData)

        weightTable = WeightTable(weightTable)
        transactions_data = data
        transactions = [
            TransactionDTO(tid=i+1, items=data, weight_table=weightTable) for i, data in enumerate(transactions_data)
        ]

        return [transactions,weightTable]
    
    def writeFile(self,filename:str,data:[ItemDto],runtime,memory_usage,lenData:int,minEXSup:float):
        folderPath = "output/WdFim"
        filePath = filename


        # Ensure the folder exists, create it if necessary
        if not os.path.exists(folderPath):
            os.makedirs(folderPath)

        # Construct the full file path
        filePath = os.path.join(folderPath, filePath)


        with open(filePath, 'w') as file:
            for i in data:
                if isinstance(i.item, frozenset):
                    file.write(str(set(i.item)) +' : '+ str(i.probability) + '\n')
                else:
                    file.write(str(i.item) +' : '+ str(i.probability) + '\n')

            
            file.write('\n' + '\n'+ '\n' + '\n')
            file.write('length' + ' : '+ str(lenData) + '\n')
            file.write('minEXSup' + ' : '+ str(minEXSup*100)+ ' %' + '\n')
            file.write('candidate' + ' : '+ str(len(data)) + '\n')
            file.write('runtime' + ' : '+ str(runtime) + ' s' + '\n')
            file.write('memory usage' + ' : '+ str(memory_usage) + ' MB'+ '\n')


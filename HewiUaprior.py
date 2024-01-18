
import os
import time
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
import psutil

from calculatoritemsetProbabilityInATransaction import calculatorItemsetProbabilityInATransaction



class HewiUaprior:
    
    def execute(self):    
        # weight_table = WeightTable()
        dataBase,filename = HewiUaprior().createDataBase()
        HewiUaprior().handleLogic(dataBase,0.1,filename)
        # mushroom = Lin2016().readFile('input/data.txt')
        # Lin2016().handleLogic(mushroom,0.1,'data.txt')
        # mushroom = Lin2016().readFile('input/mushroom.txt')
        # Lin2016().handleLogic(mushroom,0.00001,'mushroom-0,00001.txt')
        # retail = Lin2016().readFile('input/retail.txt')
        # Lin2016().handleLogic(retail,0.00001,'retail-0,00001.txt')
        # T40I10D100K = Lin2016().readFile('input/T40I10D100K.txt')
        # Lin2016().handleLogic(T40I10D100K,0.00001,'T40I10D100K-0,00001.txt')




    def handleLogic(self,dataBase: list,minEWSup: int,filename:str):
        """
        """
        print('start')
        process = psutil.Process()

        startTime = time.time()
        startMemory = process.memory_info().rss / (1024 ** 2)  # in megabytes


        transactions = dataBase[0]
        weightTable = dataBase[1]
        # weightOfSyntheticChain = weightTable.calculate_probability()
        # print(weightOfSyntheticChain)



        
        # print(weightOfSyntheticChain)
        ds = DS(tid=1, transactions=transactions)
        # syntheticChain = ds.syntheticChain
        expectedWeighted = minEWSup
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


        iubwp= HewiUaprior().calculatetIubwp(ds,tubwp)
        # print(iubwp)

        hubewis =[]
        currentLSet=[]
        hewis=[]

        for i in iubwp:
            if(i.probability>=expectedWeightedValue):
                currentLSet.append(frozenset({i.item}))
                hubewis.append(i)


        
        k=2
        globalItemSetWithSup = defaultdict(int)

        while(len(currentLSet)):
            # tinh to hop k
            ck= apriori(currentLSet,data,0.3,0.5,k,globalItemSetWithSup)
            globalItemSetWithSup=ck[2]

            hubewik=[]

            # tính iubwp trong tổ hợp k vừa tìm được
            for i in ck[0]:
                iubwp= HewiUaprior().calculatetIubwpWithCk(i,ds,tubwp)

                if(iubwp.probability >=expectedWeightedValue):
                    hubewik.append(frozenset(iubwp.item))
                    hubewis.append(iubwp)
            currentLSet=[]
            currentLSet=hubewik
            k=k+1
        


        # Calculate Expected Support of an Itemset
        for i in hubewis:
            itemsetProbabilityInATransaction= calculatorItemsetProbabilityInATransaction(i,ds)
            expectedSupportValue = expectedSupportCalculator(i, itemsetProbabilityInATransaction)
            # print(f"Expected Support of : {expectedSupportValue}")
            # print(expectedSupportValue)
        
            
            itemsetWeight = itemsetWeightCalculator(expectedSupportValue,weightTable)

            # # Calculate Expected Weighted Support of an Itemset
            expectedWeightedSupportValue = expectedWeightedSupport(itemsetWeight, expectedSupportValue)
            # # print(f"Expected Weighted Support")

            if(expectedWeightedSupportValue.probability >=expectedWeightedValue ):
                hewis.append(expectedWeightedSupportValue)
        
        endMemory = process.memory_info().rss / (1024 ** 2)  # in megabytes
        memory_usage = endMemory - startMemory

        endTime = time.time()
        runtime = endTime - startTime
        

        HewiUaprior().writeFile(filename,hewis,runtime,memory_usage,len(ds.transactions),expectedWeighted)
        
        print('done')

    def writeFile(self,filename:str,data:[ItemDto],runtime,memory_usage,lenData:int,minEXSup:float):
        folderPath = "output"
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

    def calculatetIubwp(self,ds:DS,tubwp)-> list[ItemDto]:
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

        return [transactions,weightTable],'example.txt'
    
    def readFile(self,input:str):
        data=[]
        items=[]
        with open(input, 'r') as file:
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
    







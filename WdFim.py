
from collections import defaultdict
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
        dataBase = WdFim().createDataBase()
        transactions = dataBase[0]
        weightTable = dataBase[1]
        
        # print(weightOfSyntheticChain)
        ds = DS(tid=1, transactions=transactions)
        expectedWeighted = 0.1
        expectedWeightedValue = len(ds.transactions) * expectedWeighted
        data=[]
        for i in ds.transactions:
            tidKeys=[]
            for j in i.items:
                tidKeys.append(j.item)
            data.append(set(tidKeys))
            # data.append(set(item for item in i.items)) 
        
        wfis= WdFim().calculateExpwSup(ds=ds,weightTable=weightTable,expectedWeightedValue=expectedWeightedValue)

        cwfis1 = []
  


        wfis  

        wfisk=[]
        for i in wfis:
            wfisk.append(frozenset({i.item}))

        cwfis1:list[frozenset] = []
        scwfi1:list[ItemDto] = []
        for i in weightTable.weights:
            cwfis1.append(frozenset({i}))

            scwfi1.append(ItemDto(item=i,probability=weightTable.get_weight(i)))
            print(i)
        
        scwfi1.sort(key=lambda x: x.probability)

        k=2

        while(len(wfisk)):
            # tinh to hop k
            cwfisk  = WdFim().connection(wfisk,cwfis1,k)
            cwfis1
            scwfi1

            # NCWFISk = wConnection((CWFISk-1 - WFISk-1), SCWFIS1) 
            removeItem= WdFim().removeItem(cwfis1,wfisk)
            # tạo tổ hợp B với item trong scwfi1 có popariti nhỏ hơn
            ncwfisk = WdFim().wConnection(removeItem,scwfi1,k)
            cwfis1 = cwfisk

            rcwfisk = WdFim().removeItem(data1=cwfisk,data2=ncwfisk)
            # print(rcwfisk)

            wfisk=[]
            for i in rcwfisk:
                itemsetProbabilityInATransaction= calculatorItemsetProbabilityInATransactionWithFrozenset(i,ds)
                expectedSupportValue = expectedSupportCalculatorWithFrozenset(i, itemsetProbabilityInATransaction)
                # print(f"Expected Support of : {expectedSupportValue}")
                # print(expectedSupportValue)
            
                
                itemsetWeight = itemsetWeightCalculator(expectedSupportValue,weightTable)

                # # Calculate Expected Weighted Support of an Itemset
                expectedWeightedSupportValue = expectedWeightedSupport(itemsetWeight, expectedSupportValue)
                # # print(f"Expected Weighted Support")

                if(expectedWeightedSupportValue.probability >=expectedWeightedValue ):
                    wfis.append(expectedWeightedSupportValue)  
                    wfisk.append(frozenset(expectedWeightedSupportValue.item))
            k+=1


        
        print(wfis)
        
    def removeItem(self,data1:list[frozenset],data2: list[frozenset]):
        return [item for item in data1 if item not in data2]



    def wConnection(self,wfis:list[frozenset],scwfi: list[ItemDto],length:int):
        data:list[ItemDto] =[]
        result:list[ItemDto] =[]

        data= WdFim().calculatorWeightItem(wfis,scwfi)

        for i in data:
            for j in scwfi:
                if(i.item != j.item and i.probability > j.probability):
                    result.append(frozenset(i.item).union(frozenset(j.item)))

        return result
    
    def connection(self,wfis:list[frozenset],cwfis: list[frozenset],length:int):
        return set([i.union(j) for i in cwfis for j in wfis if len(i.union(j)) == length])
    
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

        return [transactions,weightTable]
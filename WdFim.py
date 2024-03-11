
from File import File
from Utils import Utils
import WdFim
import os
import time

import psutil
from ItemDto import ItemDto

from TransactionDTO import TransactionDto
from WeightTable import WeightTable
from DS import DS
from itertools import product




class WdFim:
    
    def execute(self,dataBase: list,minEWSup: int,filename:str):    
        print('start')
        process = psutil.Process()

        startTime = time.time()
        startMemory = process.memory_info().rss / (1024 ** 2)  # in megabytes
        # weight_table = WeightTable()
        transactions = dataBase[0]
        weightTable = dataBase[1]
        
        # print(weightOfSyntheticChain)
        ds = DS(id=1, transactions=transactions)
        expectedWeighted = minEWSup
        expectedWeightedValue = len(ds.transactions) * expectedWeighted
        data=[]

        # loop từng trasaction trong ds
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
                itemsetProbabilityInATransaction= Utils().calculatorItemsetProbabilityInATransactionWithFrozenset(i,ds)
                expectedSupportValue = Utils().expectedSupportCalculatorWithFrozenset(i, itemsetProbabilityInATransaction)
                # print(f"Expected Support of : {expectedSupportValue}")
                # print(expectedSupportValue)
            
                
                itemsetWeight = Utils().itemsetWeightCalculator(expectedSupportValue,weightTable)

                # # Calculate Expected Weighted Support of an Itemset
                expectedWeightedSupportValue = Utils().expectedWeightedSupport(itemsetWeight, expectedSupportValue)
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
        

        File().writeFile(filename,WFIS,runtime,memory_usage,len(ds.transactions),expectedWeighted,"output/WdFim")
        
        print('done')    
    def calculatorRCWFISK(self,data1:list[frozenset],data2: list[frozenset]):
        """tính RCWFISK

        Args:
            data1 (list[frozenset]): list CWFISK
            data2 (list[frozenset]): list NCWFISK

        Returns:
            _type_: list RCWFISK
        """
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
        """remove item trùng nhau trong 2 list

        Args:
            data1 (list[ItemDto]): list 1 
            data2 (list[ItemDto]): list 2

        Returns:
            _type_: list item không trùng nhau
        """
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
        """tạo tổ hợp từ 2 list theo trọng số

        Args:
            removeItem (list[ItemDto]): list 1
            scwfi (list[ItemDto]): list 2
            length (int): độ dài tổ hợp

        Returns:
            result: list các tổ hợp

        """
        result:list[ItemDto] =[]

        for i in removeItem:
            for j in scwfi:
                if(i.probability > j.probability and len(frozenset(i.item).union(frozenset(j.item))) == length):
                    result.append(frozenset(i.item).union(frozenset(j.item)))

        return result
    
    def connection(self,wfis:list[ItemDto],cwfis: list[ItemDto],length:int):
        """tính tổ hợp từ các item

        Args:
            wfis (list[ItemDto]): wfis
            cwfis (list[ItemDto]): cwfis
            length (int): độ dài tổ hợp

        Returns:
            result: list tổ hợp cần tạo
        """
        return set([frozenset(i.item).union(frozenset(j.item)) for i in cwfis for j in wfis if len(frozenset(i.item).union(frozenset(j.item))) == length])
    

    
    def calculateExpwSup(self,ds:DS,weightTable:WeightTable,expectedWeightedValue:int)-> list[ItemDto]:
        """tính expwSup 

        Args:
            ds (DS): danh sach transaction trong db
            weightTable (WeightTable): weight table
            expectedWeightedValue (int): trọng số kì vọng

        Returns:
            list[ItemDto]: _description_
        """
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
            probability=item.probability * weightTable.getWeight(item.item)
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
            probability=item.probability * weightTable.getWeight(item.item)

            if(probability > expectedWeightedValue):
                expwSup.append(ItemDto(item=item.item,probability=probability))
        return expwSup
    
    
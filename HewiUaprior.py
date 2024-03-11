
import os
import time
from Apriori import Apriori
from File import File
from ItemDto import ItemDto
from TransactionDTO import TransactionDto
from Utils import Utils
from WeightTable import WeightTable
from DS import DS
import random
from collections import defaultdict
import psutil




class HewiUaprior:
    
    def execute(self,dataBase: list,minEWSup: int,filename:str):
        """_summary_

        Args:
            dataBase (list): gom dataItemSet va weight table
            minEWSup (int): min expect weight support
            filename (str): tên file output
        """
        print('start')
        process = psutil.Process()

        # lay time bat đầu chạy thuật toán
        startTime = time.time()

        # lấy memory ram bắt đầu chạy thuật toán
        startMemory = process.memory_info().rss / (1024 ** 2)  # in megabytes

        # lấy transactions tù database
        transactions = dataBase[0]

        # lấy weight table từ database
        weightTable = dataBase[1]

        # import data vào DS dto
        ds = DS(id=1, transactions=transactions)

        expectedWeighted = minEWSup
        # tính expectWeightedValue
        expectedWeightedValue = len(ds.transactions) * expectedWeighted
        
        data=[]
        # lấy item của mỗi transaction vào 1 array
        for i in ds.transactions:
            tidKeys=[]
            for j in i.items:
                tidKeys.append(j.item)
            data.append(set(tidKeys))

        tubw =[]
        tubp = []
        tubwp= []

        # lặp qua từng transaction trong transactions để tính tubw, tubp, tubwp
        for i in ds.transactions:
            tubw=i.calculateTubwt(weightTable)
            tubp=i.calculateTubpr()
            tubwp.append(tubw.probability*tubp.probability)

        # tính iubwp từ ds và tubwp
        iubwp= HewiUaprior().calculatetIubwp(ds,tubwp)

        hubewis =[]
        currentLSet=[]
        hewis=[]

        # Kiểm tra mỗi item trong iubwp có lớn hơn expectedWeightedValue
        # Thỏa điều kiện thì append vào hubewis và currentLSet 
        for i in iubwp:
            if(i.probability>=expectedWeightedValue):
                currentLSet.append(frozenset({i.item}))
                hubewis.append(i)


        
        k=2
        globalItemSetWithSup = defaultdict(int)

        # lặp cho đến currentLSet rỗng
        while(len(currentLSet)):
            # tinh to hop k bằng thuạt toán apriori
            ck= Apriori().execute(currentLSet,data,0.3,k,globalItemSetWithSup)
            globalItemSetWithSup=ck[1]

            hubewik=[]

            # tính iubwp trong tổ hợp k vừa tìm được
            for i in ck[0]:
                # tinh Iubwp với mỗi item trong ứng viên dc tạo từ thuật toán apriori
                iubwp= HewiUaprior().calculatetIubwpWithCk(i,ds,tubwp)

                # ktra iubwp co lon hơn expectedWeightedValue
                if(iubwp.probability >=expectedWeightedValue):
                    hubewik.append(frozenset(iubwp.item))
                    hubewis.append(iubwp)
            currentLSet=[]
            currentLSet=hubewik
            k=k+1
        


        # Calculate Expected Support of an Itemset
        for i in hubewis:
            # tính Itemset Probability In A Transaction
            itemsetProbabilityInATransaction= Utils().calculatorItemsetProbabilityInATransaction(i,ds)

            # tính Expected support of an itemset in D
            expectedSupportValue = Utils().expectedSupportCalculator(i, itemsetProbabilityInATransaction)
        
            # lấy weight trong weigth table
            itemsetWeight = Utils().itemsetWeightCalculator(expectedSupportValue,weightTable)

            # # Calculate Expected Weighted Support of an Itemset
            expectedWeightedSupportValue = Utils().expectedWeightedSupport(itemsetWeight, expectedSupportValue)

            #kiem tra expectedWeightedSupportValue vơi expectedWeightedValue
            if(expectedWeightedSupportValue.probability >=expectedWeightedValue ):
                hewis.append(expectedWeightedSupportValue)
        
        endMemory = process.memory_info().rss / (1024 ** 2)  # in megabytes
        memory_usage = endMemory - startMemory

        endTime = time.time()
        runtime = endTime - startTime
        

        File().writeFile(filename,hewis,runtime,memory_usage,len(ds.transactions),expectedWeighted,"output/HewiUaprior")
        
        print('done')


    def calculatetIubwp(self,ds:DS,tubwp)-> list[ItemDto]:
        """tính iubwp

        Args:
            ds (DS): ds transiction
            tubwp (_type_): tubwp

        Returns:
            list[ItemDto]: list iubwp
        """
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
    
    def calculatetIubwpWithCk(self,itemck:set,ds:DS,tubwp:list[float]):
        """_summary_

        Args:
            itemck (set): item 
            ds (DS): danh sach item trong transactions
            tubwp (_type_): tubwp

        Returns:
            Iubwp: retrunt ItemDto(item,probability)
        """
        total = 0
        # lặp qua các transaction trong DB
        for transaction in ds.transactions:
            count = 0 
            # lặp qua từng imte trong 1 transaction
            for item in transaction.items:
                # lặp qua item trong frequent itemSet 
                for i in itemck:
                    # nếu item trong frequent imteSet = item trong transaction
                    if(item.item == i):
                        # count +=1 sô lần xuất hiện
                        count+=1
            # trong 1 transaction nếu các item trong frequent imteSet xuất hiện hết thì IubwpW = tubwp của transaction đó
            if(count == len(itemck)):
                total+=tubwp[transaction.tid -1]
        # return frequent itemSet và IubwpW tương ứng 
        return ItemDto(item=itemck,probability=total)





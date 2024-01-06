
from ItemDto import ItemDto
from TidDto import TidDto
from TransactionDTO import TransactionDTO
from WeightTable import WeightTable
from DS import DS
from ExpectedSupportCalculator import expectedSupport
from ExpectedWeightedSupportCalculator import expectedWeightedSupport
from Util import getItemByLength
from Util import Apriori_gen



class Lin2016:
    
    def execute(self):    
        # weight_table = WeightTable()
        dataBase = Lin2016().createDataBase()
        transactions = dataBase[0]
        weightTable = dataBase[1]
        weightOfSyntheticChain = weightTable.calculate_probability()
        # print(weightOfSyntheticChain)



        
        # print(weightOfSyntheticChain)
        ds = DS(tid=1, transactions=transactions)
        syntheticChain = ds.syntheticChain
        expectedWeighted = 0.1
        expectedWeightedValue = len(ds.transactions) * expectedWeighted
        k=1
        tubw =[]
        for i in ds.transactions:
            tubw.append(i.calculateTubw(weightTable))

        # print('tubw : ')
        # print(tubw)

        tubp = []
        for i in ds.transactions:
            tubp.append(i.calculateTubp())
        # print('tubp')
        # print(tubp)

        # print('tubwp')
        tubwp = Lin2016().calculatetTubwp(tubp,tubw)
        # print(tubwp)

        syntheticChainByK = getItemByLength(syntheticChain,k)

        # print('iubwp')
        iubwp= Lin2016().calculatetIubwp(syntheticChainByK,ds,tubwp)
        # print(iubwp)

        HUBEWIs =[]
        HUBEWI1=[]
        for i in iubwp:
            if(i.get(list(i.keys())[0])>=expectedWeightedValue):
                HUBEWI1.append(i)
                HUBEWIs.append(i)
        k=2

        while(len(HUBEWI1)):
            syntheticChainByK = getItemByLength(syntheticChain,k)
            iubwpByK= Lin2016().calculatetIubwp(syntheticChainByK,ds,tubwp)
            HUBEWIk=[]
            for i in iubwpByK:
                if(i.get(list(i.keys())[0])>=expectedWeightedValue):
                    HUBEWIk.append(i)
                    HUBEWIs.append(i)
            HUBEWI1=HUBEWIk
            k=k+1
        
        itemsetProbabilityInATransaction = [] 
        # print('Itemset probability in a transaction')
        for i in ds.transactions:
            itemsetProbabilityInATransaction.append(i.probability)

        # print('itemset probability in a transaction')
        # print(itemsetProbabilityInATransaction)
            
        itemHUBEWIs=[]
        hewis=[]
        for i in HUBEWIs:
            itemHUBEWIs.append(list(i.keys())[0])

        # Calculate Expected Support of an Itemset
        for i in itemHUBEWIs:
            expectedSupportValue = expectedSupport([i], itemsetProbabilityInATransaction)
            # print(f"Expected Support of : {expectedSupportValue}")
            # print(expectedSupportValue)

            # Calculate Expected Weighted Support of an Itemset
            expectedWeightedSupportValue = expectedWeightedSupport(weightOfSyntheticChain, expectedSupportValue)
            # print(f"Expected Weighted Support")
            # print(expectedWeightedSupportValue)

            # print('hewi')
            hewik =Lin2016().calculatetHewis(expectedWeightedSupportValue,expectedWeightedValue)
            if(len(hewik)):
                hewis.append(hewik[0])
        
        print(HUBEWIs)
        for i in hewis:
            print([i.item,i.probability])


    
    def calculateExample():
        # weight_table = WeightTable()
        dataBase = Lin2016().createDataBase()
        transactions = dataBase[0]
        weightTable = dataBase[1]
        weightOfSyntheticChain = weightTable.calculate_probability()
        # print(weightOfSyntheticChain)



        
        # print(weightOfSyntheticChain)
        ds = DS(tid=1, transactions=transactions)
        syntheticChain = ds.syntheticChain
        expectedWeighted = 0.1
        expectedWeightedValue = len(ds.transactions) * expectedWeighted

        # print(expectedWeightedValue)

        # print(syntheticChain)
        # print(ds.tid)

        #  Calculate Itemset Weight

        # print('Itemset weight in D')
        # print(weightTable.calculate_probability())

        itemsetProbabilityInATransaction = [] 
        # print('Itemset probability in a transaction')
        for i in ds.transactions:
            itemsetProbabilityInATransaction.append(i.probability)

        # print('itemset probability in a transaction')
        # print(itemsetProbabilityInATransaction)

        # Calculate Expected Support of an Itemset
        expectedSupportValue = expectedSupport(syntheticChain, itemsetProbabilityInATransaction)
        # print(f"Expected Support of : {expectedSupportValue}")
        # print()

        # Calculate Expected Weighted Support of an Itemset
        expectedWeightedSupportValue = expectedWeightedSupport(weightOfSyntheticChain, expectedSupportValue)
        # print(f"Expected Weighted Support")
        # print(expectedWeightedSupportValue)

        print('hewi')
        hewi =Lin2016().calculatetHewis(expectedWeightedSupportValue,expectedWeightedValue)
        print(hewi)

        tubw =[]
        for i in ds.transactions:
            tubw.append(i.calculateTubw(weightTable))

        # print('tubw : ')
        # print(tubw)

        tubp = []
        for i in ds.transactions:
            tubp.append(i.calculateTubp())
        # print('tubp')
        # print(tubp)

        # print('tubwp')
        tubwp = Lin2016().calculatetTubwp(tubp,tubw)
        # print(tubwp)

        # print('iubwp')
        iubwp= Lin2016().calculatetIubwp(syntheticChain,ds,tubwp)
        # print(iubwp)

        HUBEWI = Lin2016().calculatetHubewi(iubwp,expectedWeightedValue)
        print('HUBEWI')
        print(HUBEWI)


    def calculatetHewis(self,expectedWeightedSupportValue: list[ItemDto],expectedWeightedValue:int):
        result =[]
        for i in expectedWeightedSupportValue:
            if(i.probability >=expectedWeightedValue):
                result.append(i)

        return result

    def calculatetHubewi(self,iubwp,expectedWeightedValue):
        result =[]
        for i in iubwp:
            if(i.get(list(i.keys())[0])>=expectedWeightedValue):
                result.append(i)
        sortedData = sorted(result, key=lambda x: len(list(x.keys())[0]))

        return sortedData




    def calculatetTubwp(self,tubp,tubw):
        result =[]
        for i in tubp:
            for j in tubw:
                if(list(i.keys())[0] == list(j.keys())[0]):
                    tubpValue =  i.get(list(i.keys())[0])
                    tubwValue = j.get(list(j.keys())[0])
                    tubwpValue = tubpValue * tubwValue
                    
                    result.append({list(i.keys())[0]:tubwpValue})
        return result

    def calculatetIubwp(self,syntheticChain,ds,tubwp):
        iubwp = []
        for i in syntheticChain:
            tubwpArray=[]
            for j in ds.transactions:
                for x in j.syntheticChain():
                    if(i == x):
                        tubwpTid =tubwp[j.tid-1]
                        tubwpValue =tubwpTid.get(j.tid)
                        tubwpArray.append(tubwpValue)
            if(len(tubwpArray)):
                iubwp.append({i:sum(tubwpArray)})
        return iubwp
    
    
    
    
    
    
    
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
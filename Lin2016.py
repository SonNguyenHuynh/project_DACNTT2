
from ItemDto import ItemDto
from ItemsetSupportCalculators import itemset_weight
from TidDto import TidDto
from TransactionDTO import TransactionDTO
from WeightTable import WeightTable
from DS import DS
from ExpectedSupportCalculator import expectedSupport
from ExpectedWeightedSupportCalculator import expectedWeightedSupport



class Lin2016:
    
    def lin2016(self):    
        # weight_table = WeightTable()
        dataBase = Lin2016().createDataBase()
        transactions = dataBase[0]
        weightTable = dataBase[1]
        weightOfSyntheticChain = weightTable.calculate_probability()
        print(weightOfSyntheticChain)


        
        # print(weightOfSyntheticChain)
        ds = DS(tid=1, transactions=transactions)
        syntheticChain = ds.syntheticChain
        # print(syntheticChain)
        # print(ds.tid)

        #  Calculate Itemset Weight

        # print('Itemset weight in D')
        # print(weightTable.calculate_probability())

        itemsetProbabilityInATransaction = [] 
        print('Itemset probability in a transaction')
        for i in ds.transactions:
            itemsetProbabilityInATransaction.append(i.probability)

        # print(itemsetProbabilityInATransaction)

        # Calculate Expected Support of an Itemset
        expectedSupportValue = expectedSupport(syntheticChain, itemsetProbabilityInATransaction)
        print(f"Expected Support of : {expectedSupportValue}")
        print()

        # Calculate Expected Weighted Support of an Itemset
        expectedWeightedSupportValue = expectedWeightedSupport(weightOfSyntheticChain, expectedSupportValue)
        print(f"Expected Weighted Support")
        print(expectedWeightedSupportValue)

    
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

from ExpectedSupportCalculator import expectedSupportCalculator
from ItemDto import ItemDto
from ItemsetSupportCalculators import itemsetWeight
from TidDto import TidDto
from TransactionDTO import TransactionDTO
from WeightTable import WeightTable
from DS import DS
from ExpectedWeightedSupportCalculator import expectedWeightedSupport



class Baocao2:
    
    def Baocao2(self):    
        # weight_table = WeightTable()
        dataBase = Baocao2().createDataBase()
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
        expectedSupportValue = expectedSupportCalculator(syntheticChain, itemsetProbabilityInATransaction)
        print(f"Expected Support of : {expectedSupportValue}")
        print()

        # Calculate Expected Weighted Support of an Itemset
        expectedWeightedSupportValue = expectedWeightedSupport(weightOfSyntheticChain, expectedSupportValue)
        print(f"Expected Weighted Support")
        print(expectedWeightedSupportValue)

    
    def createDataBase(self):

        weightTable = WeightTable({'A': 0.1, 'B': 0.8, 'C': 0.3, 'D': 1.0, 'E': 0.6, 'F': 1.0})
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
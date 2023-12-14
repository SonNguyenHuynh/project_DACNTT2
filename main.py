# from item import ItemDto
# from tid import TidDto
# from transaction import TransactionDto
# from weigth import WeightDto


# def main():
#    dataBase = createDataBase()

#    for index,i in enumerate(dataBase.tid,start=1):
#         print(index)
#         print([(x.item,x.probability) for x in i.transaction])

#    weightTable = createWeightTable()
#    for i in weightTable:
#         print(i.item,i.weight)
   
# def createDataBase():
#     transaction1 = TransactionDto(item=[ItemDto(item='A',probability=0.25),ItemDto(item='C',probability=0.4),ItemDto(item='E',probability=1.0)])
#     transaction2 = TransactionDto(item=[ItemDto(item='D',probability=0.35),ItemDto(item='F',probability=0.7)])
#     transaction3 = TransactionDto(item=[ItemDto(item='A',probability=0.7),ItemDto(item='B',probability=0.82),ItemDto(item='C',probability=0.9),ItemDto(item='E',probability=1.0),ItemDto(item='F',probability=0.7)])
#     transaction4 = TransactionDto(item=[ItemDto(item='D',probability=1.0),ItemDto(item='F',probability=0.5)])
#     transaction5 = TransactionDto(item=[ItemDto(item='B',probability=0.4),ItemDto(item='C',probability=0.4),ItemDto(item='D',probability=1.0)])
#     transaction6 = TransactionDto(item=[ItemDto(item='A',probability=0.8),ItemDto(item='B',probability=0.8),ItemDto(item='C',probability=1.0),ItemDto(item='F',probability=0.3)])
#     transaction7 = TransactionDto(item=[ItemDto(item='B',probability=0.8),ItemDto(item='C',probability=0.9),ItemDto(item='D',probability=0.5),ItemDto(item='E',probability=1.0)])
#     transaction8 = TransactionDto(item=[ItemDto(item='B',probability=0.65),ItemDto(item='B',probability=0.8)])
#     transaction9 = TransactionDto(item=[ItemDto(item='B',probability=0.5),ItemDto(item='D',probability=0.8),ItemDto(item='F',probability=1.0)])
#     transaction10 = TransactionDto(item=[ItemDto(item='A',probability=0.4),ItemDto(item='B',probability=1.0),ItemDto(item='C',probability=0.9),ItemDto(item='E',probability=0.85)])




#     dataBase = TidDto(transaction=[transaction1,transaction2,transaction3,transaction4,transaction5,transaction6,transaction7,transaction8,transaction9,transaction10])

#     # # Access and print the values of the DTO
#     # for index,i in enumerate(dataBase.tid,start=1):
#     #     print(index)
#     #     print([(x.item,x.probability) for x in i.transaction])
#     #     # for j in i.transaction:
#     #     #     print(i)
#     return dataBase

# def createWeightTable():
#     weightA = WeightDto(item='A',weight=0.2)
#     weightB = WeightDto(item='B',weight=0.75)
#     weightC = WeightDto(item='C',weight=0.9)
#     weightD = WeightDto(item='D',weight=1.0)
#     weightE = WeightDto(item='E',weight=0.55)
#     weightF = WeightDto(item='F',weight=0.2)

#     return [weightA,weightB,weightC,weightD,weightE,weightF] 



# if __name__ == "__main__":
#     main()


from ItemDto import ItemDto
from WeightDto import WeightDto
from TidDto import TidDto
from TransactionDTO import TransactionDTO
from WeightTable import WeightTable
from DS import DS
from ItemsetWeightCalculator import itemset_weight
from ExpectedSupportCalculator import expected_support
from ExpectedWeightedSupportCalculator import expected_weighted_support

weight_table = WeightTable()

itemset_to_check = {'A', 'D'}

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
    TransactionDTO(tid=i+1, items=data, weight_table=weight_table) for i, data in enumerate(transactions_data)
]

ds = DS(tid=1, transactions=transactions)

# Calculate Itemset Weight
itemset_weight_value = itemset_weight(itemset_to_check, ds.transactions)
print(f"Itemset Weight of {itemset_to_check}: {itemset_weight_value}")

# Calculate Expected Support of an Itemset
expected_support_value = expected_support(itemset_to_check, ds.transactions)
print(f"Expected Support of {itemset_to_check}: {expected_support_value}")

# Calculate Expected Weighted Support of an Itemset
expected_weighted_support_value = expected_weighted_support(itemset_to_check, ds.transactions)
print(f"Expected Weighted Support of {itemset_to_check}: {expected_weighted_support_value}")
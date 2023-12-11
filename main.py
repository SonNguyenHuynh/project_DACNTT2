





from item import ItemDto
from tid import TidDto
from transaction import TransactionDto
from weigth import WeightDto


def main():
   dataBase = createDataBase()

   for index,i in enumerate(dataBase.tid,start=1):
        print(index)
        print([(x.item,x.probability) for x in i.transaction])

   weightTable = createWeightTable()
   for i in weightTable:
        print(i.item,i.weight)
   
def createDataBase():
    transaction1 = TransactionDto(item=[ItemDto(item='A',probability=0.25),ItemDto(item='C',probability=0.4),ItemDto(item='E',probability=1.0)])
    transaction2 = TransactionDto(item=[ItemDto(item='D',probability=0.35),ItemDto(item='F',probability=0.7)])
    transaction3 = TransactionDto(item=[ItemDto(item='A',probability=0.7),ItemDto(item='B',probability=0.82),ItemDto(item='C',probability=0.9),ItemDto(item='E',probability=1.0),ItemDto(item='F',probability=0.7)])
    transaction4 = TransactionDto(item=[ItemDto(item='D',probability=1.0),ItemDto(item='F',probability=0.5)])
    transaction5 = TransactionDto(item=[ItemDto(item='B',probability=0.4),ItemDto(item='C',probability=0.4),ItemDto(item='D',probability=1.0)])
    transaction6 = TransactionDto(item=[ItemDto(item='A',probability=0.8),ItemDto(item='B',probability=0.8),ItemDto(item='C',probability=1.0),ItemDto(item='F',probability=0.3)])
    transaction7 = TransactionDto(item=[ItemDto(item='B',probability=0.8),ItemDto(item='C',probability=0.9),ItemDto(item='D',probability=0.5),ItemDto(item='E',probability=1.0)])
    transaction8 = TransactionDto(item=[ItemDto(item='B',probability=0.65),ItemDto(item='B',probability=0.8)])
    transaction9 = TransactionDto(item=[ItemDto(item='B',probability=0.5),ItemDto(item='D',probability=0.8),ItemDto(item='F',probability=1.0)])
    transaction10 = TransactionDto(item=[ItemDto(item='A',probability=0.4),ItemDto(item='B',probability=1.0),ItemDto(item='C',probability=0.9),ItemDto(item='E',probability=0.85)])




    dataBase = TidDto(transaction=[transaction1,transaction2,transaction3,transaction4,transaction5,transaction6,transaction7,transaction8,transaction9,transaction10])

    # # Access and print the values of the DTO
    # for index,i in enumerate(dataBase.tid,start=1):
    #     print(index)
    #     print([(x.item,x.probability) for x in i.transaction])
    #     # for j in i.transaction:
    #     #     print(i)
    return dataBase

def createWeightTable():
    weightA = WeightDto(item='A',weight=0.2)
    weightB = WeightDto(item='B',weight=0.75)
    weightC = WeightDto(item='C',weight=0.9)
    weightD = WeightDto(item='D',weight=1.0)
    weightE = WeightDto(item='E',weight=0.55)
    weightF = WeightDto(item='F',weight=0.2)

    return [weightA,weightB,weightC,weightD,weightE,weightF] 



if __name__ == "__main__":
    main()
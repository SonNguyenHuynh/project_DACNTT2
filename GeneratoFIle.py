import os
import random
from ItemDto import ItemDto
from TransactionDTO import TransactionDTO
from WeightTable import WeightTable


def readFile():
    data=[]
    items=[]
    input= 'input/T40I10D100K.txt'
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
    convertItems  = {key: round(random.uniform(0.1, 1), 2) for key in items}
    # print(convertItems)
    convertData = [[(str(item), round(random.uniform(0.1, 1), 2)) for item in sublist] for sublist in data]
    # print(convertData)

    weightTable = WeightTable(convertItems)
    transactions_data = convertData
    transactions = [
        TransactionDTO(tid=i+1, items=data, weight_table=weightTable) for i, data in enumerate(transactions_data)
    ]

    folderPath = "input/DataTest"
    filePathData = 'T40I10D100K.txt'
    filePathWeightTable = 'T40I10D100K-weight-table.txt'


    # Ensure the folder exists, create it if necessary
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)

    # Construct the full file path
    filePathData = os.path.join(folderPath, filePathData)
    filePathWeightTable = os.path.join(folderPath, filePathWeightTable)



    with open(filePathData, 'w') as file:
        for i in transactions:
            for j in i.items:
                file.write('(' + str(j.item) +','+ str(j.probability)+ ')' + ' ')
            file.write('\n')

    with open(filePathWeightTable, 'w') as file:
        for i in weightTable.weights:
            file.write('(' + str(i) +','+ str(weightTable.get_weight(i))+ ')' + ' ')


readFile()




import os
from ItemDto import ItemDto
from TransactionDTO import TransactionDto
from WeightTable import WeightTable


class File:
    def createDataBase(self,type:str):

        weightTableWdFim = WeightTable({'A': 0.1, 'B': 0.8, 'C': 0.3, 'D': 1.0, 'E': 0.6, 'F': 0.1})
        transactionsDataWdFim = [
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

        weightTableHewi = WeightTable({'A': 0.2, 'B': 0.75, 'C': 0.9, 'D': 1.0, 'E': 0.55, 'F': 0.3})

        transactions_dataHewi = [
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

        if type == 'WdFim':
            weightTable = weightTableWdFim
            transactionsData = transactionsDataWdFim
        else:
            weightTable = weightTableHewi
            transactionsData = transactions_dataHewi

        transactions = [
            TransactionDto(tid=i+1, items=data, weightTable=weightTable) for i, data in enumerate(transactionsData)
        ]

        return [transactions,weightTable],'example.txt'
    
    def readFile(self,dataFile:str,weightTableFile:str):
        data=[]
        with open(dataFile, 'r') as file:
            for line in file:
                itemList = line.split()
                dataLine = []
                for number in itemList:
                    numberValue = number.strip('()').split(',')
                    dataLine.append((str(numberValue[0]),float(numberValue[1])))
                data.append(dataLine)

        with open(weightTableFile, 'r') as file:
            for line in file:
                itemList = line.split()
                weightTable = {}
                for number in itemList:
                    numberValue = number.strip('()').split(',')
                    weightTable[str(numberValue[0])] = float(numberValue[1])

        # print(data)
        # print(items)
        # convertItems  = {key: round(random.uniform(0, 1), 2) for key in items}
        # print(convertItems)
        # convertData = [[(str(item), round(random.uniform(0, 1), 2)) for item in sublist] for sublist in data]
        # print(convertData)

        weightTable = WeightTable(weightTable)
        transactions_data = data
        transactions = [
            TransactionDto(tid=i+1, items=data, weightTable=weightTable) for i, data in enumerate(transactions_data)
        ]

        return [transactions,weightTable]
    
    def writeFile(self,filename:str,data:[ItemDto],runtime,memoryUsage,lenData:int,minEXSup:float,folderPath:str,reliableProbabilisticSupport:float):
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
            file.write('reliableProbabilisticSupport' + ' : '+ str(reliableProbabilisticSupport) + '\n')
            file.write('candidate' + ' : '+ str(len(data)) + '\n')
            file.write('runtime' + ' : '+ str(runtime) + ' s' + '\n')
            file.write('memory usage' + ' : '+ str(memoryUsage) + ' MB'+ '\n')


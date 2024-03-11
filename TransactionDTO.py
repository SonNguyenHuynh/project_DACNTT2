from typing import List, Tuple
from ItemDto import ItemDto

class TransactionDto:
    def __init__(self, tid, items: List[Tuple[str, float]], weightTable):
        self.tid = tid
        self.items = [ItemDto(item=item, probability=probability) for item, probability in items]
        self.weightTable = weightTable


    def calculateTubwt(self,weightTable):
        array =[]
        for i in self.items:
            weight =weightTable.getWeight(i.item)
            array.append(weight)
        maxWeight= max(array)
        return ItemDto(item=self.tid,probability=maxWeight) 
    
    def calculateTubpr(self):
        tubp =  max(x.probability for x in self.items)
        return ItemDto(item=self.tid,probability=tubp)
    
    def calculateIubwpr(self,weightTable):
        array =[]
        for i in self.items:
            weight =weightTable.get_weight(i.item)
            array.append(weight)
        maxWeight= max(array)
        return {self.tid:maxWeight} 
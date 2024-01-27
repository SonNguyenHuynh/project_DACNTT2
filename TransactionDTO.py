from typing import List, Tuple
from ItemDto import ItemDto
from Util import generateStrings
from WeightTable import WeightTable

class TransactionDTO:
    def __init__(self, tid, items: List[Tuple[str, float]], weight_table):
        self.tid = tid
        self.items = [ItemDto(item=item, probability=probability) for item, probability in items]
        self.weight_table = weight_table


    def syntheticChain(self):
        listString= []
        for item in self.items:
            listString.append(item.item)
        syntheticChain = sorted(generateStrings(self,listString))
        return syntheticChain
    
    def calculateTubw(self,weightTable):
        array =[]
        for i in self.items:
            weight =weightTable.get_weight(i.item)
            array.append(weight)
        maxWeight= max(array)
        return ItemDto(item=self.tid,probability=maxWeight) 
    
    def calculateTubp(self):
        tubp =  max(x.probability for x in self.items)
        return ItemDto(item=self.tid,probability=tubp)
    
    def calculateIubwp(self,weightTable):
        array =[]
        for i in self.items:
            weight =weightTable.get_weight(i.item)
            array.append(weight)
        maxWeight= max(array)
        return {self.tid:maxWeight} 
from typing import List, Tuple
from ItemDto import ItemDto
from Util import generate_strings
from WeightTable import WeightTable

class TransactionDTO:
    def __init__(self, tid, items: List[Tuple[str, float]], weight_table):
        self.tid = tid
        self.items = [ItemDto(item=item, probability=probability) for item, probability in items]
        self.weight_table = weight_table
        self.probability = self.calculate_probability()

    def syntheticChain(self):
        listString= []
        for item in self.items:
            listString.append(item.item)
        syntheticChain = sorted(generate_strings(self,listString))
        return syntheticChain

    def calculate_probability(self) -> float:
        listString= []
        for item in self.items:
            listString.append(item.item)
        syntheticChain = sorted(generate_strings(self,listString))
        
        result= {}
        for i in syntheticChain:
            total = 1
            for j in i:
                for x in self.items:
                    if x.item == j :
                        total *= x.probability
            result.update({i: total})
        return result
    
    
    def calculateTubw(self,weightTable):
        array =[]
        for i in self.items:
            weight =weightTable.get_weight(i.item)
            array.append(weight)
        maxWeight= max(array)
        return {self.tid:maxWeight} 
    
    def calculateTubp(self):
        tubp =  max(x.probability for x in self.items)
        return {self.tid:tubp}
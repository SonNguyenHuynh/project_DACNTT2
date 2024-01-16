from typing import List, Set
from ItemDto import ItemDto
from TransactionDTO import TransactionDTO
from WeightTable import WeightTable

def itemsetWeightCalculator(itemset: ItemDto, weightTable: WeightTable):
    total = 0
    for item in itemset.item:
        value=weightTable.get_weight(item=item)
        total += value
        
    return ItemDto(item=itemset.item,probability=total/len(itemset.item))
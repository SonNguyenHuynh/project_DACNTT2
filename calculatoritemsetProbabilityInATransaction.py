from typing import List, Set
from DS import DS
from ItemDto import ItemDto

def calculatorItemsetProbabilityInATransaction(itemset: ItemDto, ds:DS):
    result = []
    total = 1
    for transaction in ds.transactions:
        total = 1
        count = 0

        for itemdto in transaction.items:
            for item in itemset.item:
                if(itemdto.item == item):
                    count +=1
                    total *= itemdto.probability
        if(count== len(itemset.item)):
            result.append(ItemDto(item=itemset.item,probability=total))
    return result
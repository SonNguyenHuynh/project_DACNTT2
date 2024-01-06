from typing import List, Set
from ItemDto import ItemDto
from TransactionDTO import TransactionDTO

def expectedSupport(itemset: Set[str], itemsetProbabilityInATransaction: [ItemDto]):
    result=[]
    for i in itemset:
        total = 0
        for j in itemsetProbabilityInATransaction:
            item = j.get(i)
            if(item):
                total+=item
        result.append(ItemDto(item=i,probability=total))
    return result
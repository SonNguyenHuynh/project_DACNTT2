from typing import List, Set
from ItemDto import ItemDto
from TransactionDTO import TransactionDTO

def expectedSupportCalculator(itemset: ItemDto, itemsetProbabilityInATransactions: [[ItemDto]]):
    total = 0
    for itemsetProbabilityInATransaction in itemsetProbabilityInATransactions:
        for item in itemsetProbabilityInATransaction:
            if(item.item == itemset.item):
                total += item.probability
    return ItemDto(item=itemset.item,probability=total)
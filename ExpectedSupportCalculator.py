from typing import List, Set
from ItemDto import ItemDto
from TransactionDTO import TransactionDTO

def expectedSupportCalculator(itemset: ItemDto, itemsetProbabilityInATransactions: [ItemDto]):
    total = 0
    for itemsetProbabilityInATransaction in itemsetProbabilityInATransactions:
        total +=itemsetProbabilityInATransaction.probability
    return ItemDto(item=itemset.item,probability=total)
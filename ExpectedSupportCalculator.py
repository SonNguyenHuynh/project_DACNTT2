from typing import List, Set
from ItemDto import ItemDto
from TransactionDTO import TransactionDTO

def expectedSupportCalculator(itemset: ItemDto, itemsetProbabilityInATransactions: [ItemDto]):
    """tính Expected support of an itemset in D

    Args:
        itemset (ItemDto): itemSet
        itemsetProbabilityInATransactions (ItemDto]): itemset Probability In A Transactions

    Returns:
        _type_: Expected support
    """
    total = 0
    # tổng itemset Probability trong các transaction  
    for itemsetProbabilityInATransaction in itemsetProbabilityInATransactions:
        total +=itemsetProbabilityInATransaction.probability
    return ItemDto(item=itemset.item,probability=total)

def expectedSupportCalculatorWithFrozenset(itemset: frozenset, itemsetProbabilityInATransactions: [ItemDto]):
    """tính Expected support of an itemset in D

    Args:
        itemset (frozenset): itemSet
        itemsetProbabilityInATransactions (ItemDto]): itemset Probability In A Transactions

    Returns:
        _type_: Expected support
    """
    total = 0
    for itemsetProbabilityInATransaction in itemsetProbabilityInATransactions:
        total +=itemsetProbabilityInATransaction.probability
    return ItemDto(item=itemset,probability=total)
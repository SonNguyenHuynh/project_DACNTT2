from typing import List, Set
from TransactionDTO import TransactionDTO

def expected_support(itemset: Set[str], transactions: List[TransactionDTO]) -> float:
    return sum(transaction.probability * (itemset.issubset(item.item for item in transaction.items)) for transaction in transactions)

def itemsetWeight(itemset: Set[str], transactions: List[TransactionDTO]) -> float:
    total_weight = 0.0
    total_items = 0

    for transaction in transactions:
        for item in transaction.items:
            if item.item in itemset:
                total_weight += transaction.weight_table.get_weight(item.item)
                total_items += 1

    if total_items == 0:
        return 0.0
    else:
        return total_weight / total_items

from typing import List, Set
from TransactionDTO import TransactionDTO

def expected_support(itemset: Set[str], transactions: List[TransactionDTO]) -> float:
    return sum(transaction.probability * (itemset.issubset(item.item for item in transaction.items)) for transaction in transactions)

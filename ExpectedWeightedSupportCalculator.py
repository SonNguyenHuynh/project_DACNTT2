# ExpectedWeightedSupportCalculator.py
from typing import List, Set
from TransactionDTO import TransactionDTO
from ItemsetSupportCalculators import expected_support, itemset_weight

def expected_weighted_support(itemset: Set[str], transactions: List[TransactionDTO]) -> float:
    exp_support = expected_support(itemset, transactions)
    itemset_weight_value = itemset_weight(itemset, transactions)

    return exp_support * itemset_weight_value

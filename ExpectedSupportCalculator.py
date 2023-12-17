from typing import List, Set
from TransactionDTO import TransactionDTO

def expectedSupport(itemset: Set[str], itemsetProbabilityInATransaction: []):
    result=[]
    for i in itemset:
        total = 0
        for j in itemsetProbabilityInATransaction:
            item = j.get(i)
            if(item):
                total+=item
        result.append({i:total})
    return result
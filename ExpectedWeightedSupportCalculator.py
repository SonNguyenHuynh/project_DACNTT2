# ExpectedWeightedSupportCalculator.py
from typing import List, Set
from TransactionDTO import TransactionDTO
from ItemsetSupportCalculators import expected_support, itemset_weight

def expectedWeightedSupport(weight: [], expectedSupportValueList: []):
    # print(weight)
    # print(expectedSupportValueList)

    result =[]
    for i in weight:
        for j in expectedSupportValueList:
            if(list(i.keys())[0] == list(j.keys())[0]):
                weightValue =  i.get(list(i.keys())[0])
                expectedSupportValue = j.get(list(j.keys())[0])
                expectedWeightedSupport = weightValue * expectedSupportValue
                
                result.append({list(i.keys())[0]:expectedWeightedSupport})
    return result
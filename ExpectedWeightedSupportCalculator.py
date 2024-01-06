# ExpectedWeightedSupportCalculator.py
from typing import List, Set
from ItemDto import ItemDto
from TransactionDTO import TransactionDTO
from ItemsetSupportCalculators import expected_support, itemsetWeight

def expectedWeightedSupport(weight: list[str], expectedSupportValueList: list[ItemDto]):
    # print(weight)
    # print(expectedSupportValueList)

    result =[]
    for i in weight:
        for j in expectedSupportValueList:
            if(list(i.keys())[0] == j.item):
                weightValue =  i.get(list(i.keys())[0])
                expectedSupportValue = j.probability
                expectedWeightedSupport = weightValue * expectedSupportValue
                
                result.append(ItemDto(item=j.item,probability=expectedWeightedSupport) )
    return result
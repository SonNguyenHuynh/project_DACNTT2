# ExpectedWeightedSupportCalculator.py
from typing import List, Set
from ItemDto import ItemDto
from TransactionDTO import TransactionDTO
from ItemsetSupportCalculators import expected_support, itemsetWeight

def expectedWeightedSupport(itemsetWeight: ItemDto, expectedSupportValue:ItemDto):
    # print(weight)
    # print(expectedSupportValueList)
    return ItemDto(item=itemsetWeight.item,probability=itemsetWeight.probability * expectedSupportValue.probability)
# ExpectedWeightedSupportCalculator.py
from typing import List, Set
from ItemDto import ItemDto
from TransactionDTO import TransactionDTO
from ItemsetSupportCalculators import expected_support, itemsetWeight

def expectedWeightedSupport(itemsetWeight: ItemDto, expectedSupportValue:ItemDto):
    """tính expected Weighted Support

    Args:
        itemsetWeight (ItemDto): weight frequent itemSet
        expectedSupportValue (ItemDto): expectedSupportValue

    Returns:
        _type_: expectedWeightedSupport
    """
    return ItemDto(item=itemsetWeight.item,probability=itemsetWeight.probability * expectedSupportValue.probability)
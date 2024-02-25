from typing import List, Set
from ItemDto import ItemDto
from TransactionDTO import TransactionDTO
from WeightTable import WeightTable

def itemsetWeightCalculator(itemset: ItemDto, weightTable: WeightTable):
    """lấy itemSet Weight

    Args:
        itemset (ItemDto): frequent itemSet
        weightTable (WeightTable): weight table

    Returns:
        _type_: weight itemSet
    """
    total = 0
    #lap cac item trong frequent itemSet
    for item in itemset.item:
        # get weight item set 
        value=weightTable.get_weight(item=item)
        # get tỏng
        total += value
    # item và total weight / length itemSet
    return ItemDto(item=itemset.item,probability=total/len(itemset.item))
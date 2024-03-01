from typing import List, Set
from DS import DS
from ItemDto import ItemDto

def calculatorItemsetProbabilityInATransaction(itemset: ItemDto, ds:DS):
    """tính toán ItemsetProbabilityInATransaction

    Args:
        itemset (ItemDto): frequent itemSet
        ds (DS): ds transaction

    Returns:
        result: ItemsetProbabilityInATransaction
    """
    result = []
    total = 1

    # lặp qua cac transaction trong ds 
    for transaction in ds.transactions:
        total = 1
        count = 0
        # lặp qua các item trong transaction
        for itemdto in transaction.items:
            # lặp qua cac item tron frequent itemSet
            for item in itemset.item:
                # nếu item trong frequent itemSet = item trong transaction
                if(itemdto.item == item):
                    count +=1
                    total *= itemdto.probability
        # count = độ rộng của frequent itemSet
        if(count== len(itemset.item)):
            # thêm vào mảng kết quả
            result.append(ItemDto(item=itemset.item,probability=total))
    
    return result


def calculatorItemsetProbabilityInATransactionWithFrozenset(itemset: frozenset, ds:DS):
    """tính toán ItemsetProbabilityInATransaction

    Args:
        itemset (ItemDto): frequent itemSet
        ds (DS): ds transaction

    Returns:
        result: ItemsetProbabilityInATransaction
    """
    result = []
    total = 1
    for transaction in ds.transactions:
        total = 1
        count = 0

        for itemdto in transaction.items:
            for item in itemset:
                if(itemdto.item == item):
                    count +=1
                    total *= itemdto.probability
        if(count== len(itemset)):
            result.append(ItemDto(item=itemset,probability=total))
    return result
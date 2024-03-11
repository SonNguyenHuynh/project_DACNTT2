from typing import List, Set
from itertools import combinations

from csv import reader
from collections import defaultdict
from itertools import chain, combinations
from DS import DS

from ItemDto import ItemDto
from TransactionDTO import TransactionDto
from WeightTable import WeightTable

class Utils:

    def expectedSupportCalculator(self,itemset: ItemDto, itemsetProbabilityInATransactions: [ItemDto]):
        """tính Expected support of an itemset in D

        Args:
            itemset (ItemDto): itemSet
            itemsetProbabilityInATransactions (ItemDto]): itemset Probability In A Transactions

        Returns:
            _type_: Expected support
        """
        total = 0
        # tổng itemset Probability trong các transaction  
        for itemsetProbabilityInATransaction in itemsetProbabilityInATransactions:
            total +=itemsetProbabilityInATransaction.probability
        return ItemDto(item=itemset.item,probability=total)

    def expectedSupportCalculatorWithFrozenset(self,itemset: frozenset, itemsetProbabilityInATransactions: [ItemDto]):
        """tính Expected support of an itemset in D

        Args:
            itemset (frozenset): itemSet
            itemsetProbabilityInATransactions (ItemDto]): itemset Probability In A Transactions

        Returns:
            _type_: Expected support
        """
        total = 0
        for itemsetProbabilityInATransaction in itemsetProbabilityInATransactions:
            total +=itemsetProbabilityInATransaction.probability
        return ItemDto(item=itemset,probability=total)

    def expectedWeightedSupport(self,itemsetWeight: ItemDto, expectedSupportValue:ItemDto):
        """tính expected Weighted Support

        Args:
            itemsetWeight (ItemDto): weight frequent itemSet
            expectedSupportValue (ItemDto): expectedSupportValue

        Returns:
            _type_: expectedWeightedSupport
        """
        return ItemDto(item=itemsetWeight.item,probability=itemsetWeight.probability * expectedSupportValue.probability)


    def itemsetWeight(itemset: Set[str], transactions: List[TransactionDto]) -> float:
        total_weight = 0.0
        total_items = 0

        for transaction in transactions:
            for item in transaction.items:
                if item.item in itemset:
                    total_weight += transaction.weightTable.get_weight(item.item)
                    total_items += 1

        if total_items == 0:
            return 0.0
        else:
            return total_weight / total_items

    def itemsetWeightCalculator(self,itemset: ItemDto, weightTable: WeightTable):
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
            value=weightTable.getWeight(item=item)
            # get tỏng
            total += value
        # item và total weight / length itemSet
        return ItemDto(item=itemset.item,probability=total/len(itemset.item))
    

    def calculatorItemsetProbabilityInATransaction(self,itemset: ItemDto, ds:DS):
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


    def calculatorItemsetProbabilityInATransactionWithFrozenset(self,itemset: frozenset, ds:DS):
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
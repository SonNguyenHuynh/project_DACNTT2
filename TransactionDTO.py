from typing import List, Tuple
from ItemDto import ItemDto
from WeightTable import WeightTable

class TransactionDTO:
    def __init__(self, tid, items: List[Tuple[str, float]], weight_table):
        self.tid = tid
        self.items = [ItemDto(item=item, probability=probability) for item, probability in items]
        self.weight_table = weight_table
        self.probability = self.calculate_probability()

    def calculate_probability(self) -> float:
        return sum(item.probability for item in self.items)

    def get_weighted_support(self, itemset) -> float:
        return sum(self.weight_table.get_weight(item.item) * (item.item in itemset) for item in self.items)

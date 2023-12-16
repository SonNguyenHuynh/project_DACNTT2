
from ItemDto import ItemDto
from ItemsetSupportCalculators import itemset_weight
from TidDto import TidDto
from TransactionDTO import TransactionDTO
from WeightTable import WeightTable
from DS import DS
from ExpectedSupportCalculator import expectedSupport
from ExpectedWeightedSupportCalculator import expectedWeightedSupport
from Lin2016 import Lin2016
from BaoCao2 import Baocao2

def main():
    # lint2016 = Lin2016().lin2016()
    baocao2 = Baocao2().Baocao2()

if __name__ == "__main__":
    main()



# weight_table = WeightTable()

# itemset_to_check = {'A', 'D'}

# transactions_data = [
#     [('A', 0.8), ('B', 0.4), ('D', 1.0)],
#     [('B', 0.3), ('F', 0.7)],
#     [('B', 0.7), ('C', 0.9), ('E', 1.0), ('F', 0.7)],
#     [('E', 1.0), ('F', 0.5)],
#     [('A', 0.6), ('C', 0.4), ('D', 1.0)],
#     [('A', 0.8), ('B', 0.8), ('C', 1.0), ('F', 0.3)],
#     [('A', 0.8), ('C', 0.9), ('D', 0.5), ('E', 1.0)],
#     [('C', 0.6), ('E', 0.4)],
#     [('A', 0.5), ('D', 0.8), ('F', 1.0)],
#     [('A', 0.7), ('B', 1.0), ('C', 0.9), ('E', 0.8)],
# ]

# transactions = [
#     TransactionDTO(tid=i+1, items=data, weight_table=weight_table) for i, data in enumerate(transactions_data)
# ]

# ds = DS(tid=1, transactions=transactions)
# print(ds.tid)
# Calculate Itemset Weight
# itemset_weight_value = itemset_weight(itemset_to_check, ds.transactions)
# print(f"Itemset Weight of {itemset_to_check}: {itemset_weight_value}")

# # Calculate Expected Support of an Itemset
# expected_support_value = expected_support(itemset_to_check, ds.transactions)
# print(f"Expected Support of {itemset_to_check}: {expected_support_value}")

# # Calculate Expected Weighted Support of an Itemset
# expected_weighted_support_value = expected_weighted_support(itemset_to_check, ds.transactions)
# print(f"Expected Weighted Support of {itemset_to_check}: {expected_weighted_support_value}")
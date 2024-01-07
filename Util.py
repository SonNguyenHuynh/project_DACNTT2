from itertools import combinations

def generateStrings(self,characters):
    result = []
    def generate_helper(current_string, index):
        if index == len(characters):
            if current_string:  # Only append non-empty strings
                result.append(current_string)
            return
        # Include the character at the current index
        generate_helper(current_string + characters[index], index + 1)
        # Exclude the character at the current index
        generate_helper(current_string, index + 1)
    generate_helper('', 0)

    return result

def getItemByLength(characters: list[str],k:int):
    result = [combo for combo in characters if len(combo) == k]
    return result

def AprioriGen(frequent_itemsets_k):
    candidate_itemsets_kplus1 = []
    num_itemsets = len(frequent_itemsets_k)

    for i in range(num_itemsets):
        for j in range(i + 1, num_itemsets):
            candidate_itemset = list(set(frequent_itemsets_k[i]).union(frequent_itemsets_k[j]))

            if all(set(subset) in frequent_itemsets_k for subset in combinations(candidate_itemset, len(candidate_itemset) - 1)):
                candidate_itemsets_kplus1.append(sorted(candidate_itemset))

    return candidate_itemsets_kplus1


def AprioriGen(frequent_itemsets_kminus1):
    """
    Generate candidate itemsets of size k from frequent itemsets of size k-1.

    Parameters:
    - frequent_itemsets_kminus1: A list of frequent itemsets of size k-1.

    Returns:
    - candidate_itemsets: A list of candidate itemsets of size k.
    """

    candidate_itemsets = []

    # Join step: Joining two frequent itemsets of size k-1 to create a candidate itemset of size k
    for i in range(len(frequent_itemsets_kminus1)):
        for j in range(i + 1, len(frequent_itemsets_kminus1)):
            itemset1 = frequent_itemsets_kminus1[i]
            itemset2 = frequent_itemsets_kminus1[j]

            # Check if the first k-2 elements are the same
            if itemset1[:-1] == itemset2[:-1]:
                # Create a new candidate itemset by combining the two frequent itemsets
                candidate_itemset = itemset1 + [itemset2[-1]]

                # Pruning step: Check if all subsets of the candidate itemset are frequent
                if all(subset in frequent_itemsets_kminus1 for subset in getSubsets(candidate_itemset)):
                    candidate_itemset=  ''.join(candidate_itemset)

                    candidate_itemsets.append(candidate_itemset)

    return candidate_itemsets

def getSubsets(itemset):
    """
    Generate all non-empty subsets of an itemset.

    Parameters:
    - itemset: A list representing an itemset.

    Returns:
    - subsets: A list of all non-empty subsets of the itemset.
    """
    subsets = []
    for i in range(len(itemset)):
        subsets.append(itemset[:i] + itemset[i+1:])
    return subsets

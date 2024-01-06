from itertools import combinations

def generateStrings(self,characters):
    result = []
    sort = []
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

    for i in result:
        sort.append(''.join(map(str, sorted(i))))
    return sorted(sort)

def getItemByLength(characters: list[str],k:int):
    result = [combo for combo in characters if len(combo) == k]
    return result

def Apriori_gen(frequent_itemsets_k):
    candidate_itemsets_kplus1 = []
    num_itemsets = len(frequent_itemsets_k)

    for i in range(num_itemsets):
        for j in range(i + 1, num_itemsets):
            candidate_itemset = list(set(frequent_itemsets_k[i]).union(frequent_itemsets_k[j]))

            if all(set(subset) in frequent_itemsets_k for subset in combinations(candidate_itemset, len(candidate_itemset) - 1)):
                candidate_itemsets_kplus1.append(sorted(candidate_itemset))

    return candidate_itemsets_kplus1

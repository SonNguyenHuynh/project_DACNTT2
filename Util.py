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

from csv import reader
from collections import defaultdict
from itertools import chain, combinations

def dataToCSV(fname):
    first = True
    currentID = 1
    with open(fname, 'r') as dataFile, open(fname + '.csv', 'w') as outputCSV:
        for line in dataFile:
            nums = line.split()
            itemSetID = nums[1]
            item = nums[2]
            if(int(itemSetID) == currentID):
                if(first):
                    outputCSV.write(item)
                else:
                    outputCSV.write(',' + item)
                first = False
            else:
                outputCSV.write('\n' + item)
                currentID += 1


def powerset(s):
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s)))


def getFromFile(fname):
    itemSets = []
    itemSet = set()

    with open(fname, 'r') as file:
        csv_reader = reader(file,delimiter=',')
        for line in csv_reader:
            line = list(filter(None, line))
            record = set(line)
            for item in record:
                itemSet.add(frozenset([item]))
            itemSets.append(record)
    return itemSet, itemSets


def getAboveMinSup(itemSet:set, itemSetList:[set], minSup:float, globalItemSetWithSup:defaultdict(int)):
    """_summary_

    Args:
        itemSet (set): hubewis with k-1
        itemSetList (set]): danh sách item in transactions
        minSup (float): minSupport
        globalItemSetWithSup (defaultdict): count sô lần xuất hiện của item trong transactions

    Returns:
        freqItemSet: list item xuất hiện thường xuyên
    """
    freqItemSet = set()
    localItemSetWithSup = defaultdict(int)

    # lặp mỗi item trong itemSet
    for item in itemSet:
        #lăp mỗi itemSet trong itemSetlist
        for itemSet in itemSetList:
            # nếu item xuất hiện trong itemSet
            if item.issubset(itemSet):
                # cộng 1 lần trong hiện cua item trong globalItemSetWithSup
                globalItemSetWithSup[item] += 1
                # cộng 1 lần trong hiện cua item trong localItemSetWithSup
                localItemSetWithSup[item] += 1

    # lăp item trong localItemSetWithSup
    for item, supCount in localItemSetWithSup.items():
        # tinh phan tram xuat hiện của item trong transactions
        support = float(supCount / len(itemSetList))
        # nếu phần trăm > minSup thì item được cho là xuất hiện thường xuyên
        if(support >= minSup):
            freqItemSet.add(item)
    # trả về list item xuất hiện thường xuyên
    return freqItemSet


def getUnion(itemSet, length:int):
    return set([i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length])


def pruning(candidateSet:set(), prevFreqSet:set(), length:int):
    """_summary_

    Args:
        candidateSet (set): danh sach ứng viên length = k
        prevFreqSet (set): item xuất hiện thường xuyên length = k-1
        length (int): length k-1

    Returns:
        tempCandidateSet: tập ứng viên sau khi cắt giảm
    """
    tempCandidateSet = candidateSet.copy()
    # lăp item trong candidateSet
    for item in candidateSet:
        subsets = combinations(item, length)
        for subset in subsets:
            # nếu tập hợp con không nằm trong tập hợp K-thường xuyên nhận được trước đó thì hãy xóa tập hợp đó
            if(frozenset(subset) not in prevFreqSet):
                tempCandidateSet.remove(item)
                break
    return tempCandidateSet



def getItemSetFromList(itemSetList):
    tempItemSet = set()

    for itemSet in itemSetList:
        for item in itemSet:
            tempItemSet.add(frozenset([item]))

    return tempItemSet



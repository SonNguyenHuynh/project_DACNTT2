from csv import reader
from collections import defaultdict
from itertools import chain, combinations
from optparse import OptionParser



class Apriori:

    def execute(self,C1ItemSet: list[frozenset],itemSetList:list[set], minSup:float,k:int,globalItemSetWithSup:defaultdict(int)):
        """_summary_

        Args:
            C1ItemSet (_type_): hubewis with k-1 
            itemSetList (_type_): danh sách item in transactions
            minSup (_type_): minSupport
            minConf (_type_): min Confident
            k (_type_): độ rộng của item 
            globalItemSetWithSup (defaultdict): count sô lần xuất hiện của item trong transactions

        Returns:
            globalFreqItemSet[k]: ItemSet length k xuất hiện thường xuyên, 
            globalItemSetWithSup: count sô lần xuất hiện của item trong transactions
        """

        globalFreqItemSet = dict()

        # tính item xuất hiện thường xuyên > minSup
        L1ItemSet = Apriori().getAboveMinSup(
            C1ItemSet, itemSetList, minSup, globalItemSetWithSup)
        currentLSet = L1ItemSet


        # tạo ứng viên có length k với item length k-1 xuất hiện thường xuyên
        candidateSet = Apriori().getUnion(currentLSet, k)
        # Thực hiện kiểm tra tập hợp con và loại bỏ các tập hợp con đã được cắt bớt
        candidateSet = Apriori().pruning(candidateSet, currentLSet, k-1)
        # tính  lại item xuất hiện thường xuyên sau khi cắt giảm ứng viên  > minSup
        currentLSet = Apriori().getAboveMinSup(
            candidateSet, itemSetList, minSup, globalItemSetWithSup)
        globalFreqItemSet[k] = currentLSet

        return globalFreqItemSet[k] ,globalItemSetWithSup


    def getAboveMinSup(self,itemSet:set, itemSetList:[set], minSup:float, globalItemSetWithSup:defaultdict(int)):
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


    def getUnion(self,itemSet, length:int):
        return set([i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length])


    def pruning(self,candidateSet:set(), prevFreqSet:set(), length:int):
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
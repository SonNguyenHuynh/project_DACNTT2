from csv import reader
from collections import defaultdict
from itertools import chain, combinations
from optparse import OptionParser

from Util import  getAboveMinSup, getUnion, pruning




def apriori(C1ItemSet: list[frozenset],itemSetList:list[set], minSup:float,k:int,globalItemSetWithSup:defaultdict(int)):
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
    L1ItemSet = getAboveMinSup(
        C1ItemSet, itemSetList, minSup, globalItemSetWithSup)
    currentLSet = L1ItemSet


    # tạo ứng viên có length k với item length k-1 xuất hiện thường xuyên
    candidateSet = getUnion(currentLSet, k)
    # Thực hiện kiểm tra tập hợp con và loại bỏ các tập hợp con đã được cắt bớt
    candidateSet = pruning(candidateSet, currentLSet, k-1)
    # tính  lại item xuất hiện thường xuyên sau khi cắt giảm ứng viên  > minSup
    currentLSet = getAboveMinSup(
        candidateSet, itemSetList, minSup, globalItemSetWithSup)
    globalFreqItemSet[k] = currentLSet

    return globalFreqItemSet[k] ,globalItemSetWithSup


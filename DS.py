from TransactionDTO import TransactionDTO
from Util import generate_strings

class DS:
    def __init__(self, tid, transactions):
        self.tid = tid
        self.transactions = transactions
        self.syntheticChain = self.getSyntheticChain()

    def getSyntheticChain(self):
        listChart = []
        for i in self.transactions:
            for j in i.items:
                listChart.append(j.item)
        return sorted(generate_strings(self,list(dict.fromkeys(listChart))))
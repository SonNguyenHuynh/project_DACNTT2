from Util import AprioriGen


class WeightTable:
    def __init__(self,weight):
        self.weights = weight
        # self.weights = {'A': 0.1, 'B': 0.8, 'C': 0.3, 'D': 1.0, 'E': 0.6, 'F': 1.0}


    def get_weight(self, item):
        return self.weights.get(item, 0.0)

    def calculate_probability(self):
        listString= list(self.weights.keys())
        syntheticChain = AprioriGen(self,listString)
        
        result= []
        for i in syntheticChain:
            total = 0
            for j in i:
                total = total + self.get_weight(j)
            ave = total / len(i)
            result.append({i: ave})
        return result
    
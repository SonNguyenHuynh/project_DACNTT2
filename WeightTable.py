
class WeightTable:
    def __init__(self,weight:set):
        self.weights = weight
        # self.weights = {'A': 0.1, 'B': 0.8, 'C': 0.3, 'D': 1.0, 'E': 0.6, 'F': 1.0}


    def getWeight(self, item):
        return self.weights.get(item, 0.0)

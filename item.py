class ItemDto:
    item: str
    probability: str = ''

    def __init__(self, item,probability):
        self.item = item 
        self.probability = probability

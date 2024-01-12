class Stock:
    def __init__(self, price: float):
        self.price = price
    
    def getPriceInformation(self, prices: list):
        return [price - self.price for price in prices]
    
    def getReturn(self, price: float):
        return price - self.price
import numpy as np

class Portfolio:
    def __init__(self, options: list):
        self.options = options
        cost_per_trade = np.sum([x.premium for x in self.options])
        self.cost = cost_per_trade
        print("Cost per trade: ", cost_per_trade)

    def getPriceInformation(self, prices: list):
        outputs = [0] * len(prices)
        for option in self.options:
            outputs = [x + y for x, y in zip(outputs, option.getPriceInformation(prices))]
        return outputs
    
    def getReturn(self, price: float, option_allocation: float):
        sum = 0

        num_of_trades = np.floor(option_allocation / self.cost)
        
        for option in self.options:
            sum += option.getReturn(price) * num_of_trades
        
        return sum
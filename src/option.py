class OptionContract:
    def __init__(self, strike: float, premium: float, option_type: str, side: str):
        self.strike = strike
        self.premium = premium
        self.option_type = option_type
        self.side = side
    
    def getPriceInformation(self, prices: list):
        if(self.option_type == 'Call'):
            if(self.side == 'Long'):
                return [max(0, price - self.strike) - self.premium for price in prices]
            else:
                return [self.premium - max(0, price - self.strike) for price in prices]
        else:
            if(self.side == 'Long'):
                return [max(0, self.strike - price) - self.premium for price in prices]
            else:
                return [self.premium - max(0, self.strike - price) for price in prices]
    
    def getReturn(self, price: float):
        if(self.option_type == 'Call'):
            if(self.side == 'Long'):
                return max(0, price - self.strike) - self.premium
            else:
                return self.premium - max(0, price - self.strike)
        else:
            if(self.side == 'Long'):
                return max(0, self.strike - price) - self.premium
            else:
                return self.premium - max(0, self.strike - price)
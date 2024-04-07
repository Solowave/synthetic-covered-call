import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm 

from .algorithms import binarySearch
from .option import OptionContract

class Portfolio:
    def __init__(self, options_data, options: list):
        self.options_data = options_data

        tempOptions = []

        for (_strike, expiration, option_type, side) in options:
            STRIKE, STRIKE_INDEX = self.getStrikeNearPrice(options_data['call_strikes'], _strike)
            
            sideFormatted = 'bids' if side == 'long' else 'asks'

            OPTION_PREMIUM = options_data[option_type.lower() + '_' + sideFormatted][STRIKE_INDEX]
            
            while(OPTION_PREMIUM == None):
                STRIKE_INDEX += 1
                OPTION_PREMIUM = options_data[option_type.lower() + '_' + sideFormatted][STRIKE_INDEX]
                STRIKE = options_data[option_type.lower() + '_strikes'][STRIKE_INDEX]
            
            tempOptions.append(
                OptionContract(STRIKE, OPTION_PREMIUM, option_type, side)
            )

        self.options = tempOptions

        cost_per_trade = np.sum([x.premium for x in self.options])
        
        self.cost = cost_per_trade
        self.log()

    def log(self):
        print("Portfolio:")
        print("Cost per trade: ", self.cost)
        for option in self.options:
            print("Strike:", option.strike, "Premium:", option.premium, "Type:", option.option_type, "Side:", option.side)

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
    
    def draw(self, prices: list, price: float, std:float, expiration: str, STD_WIDTH=3, showProbability=False, showMarkers=False):
        fig, ax1 = plt.subplots()
        ax1.title.set_text("Synthetic Covered Call | Exp: " + expiration)

        values = self.getPriceInformation(prices)

        # Binary search to find 0 in values
        intersection = binarySearch(values, 0)

        # print("Intersection: $", prices[intersection])

        ax1.plot(prices, values)
        ax1.set_xlabel('Share Price')
        ax1.set_ylabel('Returns', color='black')
        ax1.tick_params(axis='y', labelcolor='black')

        if showMarkers:
            # ax1.axvline(x=prices[intersection], color='r', linestyle='--')
            ax1.axvline(x=price, color='g', linestyle='--')

        if showProbability:
            ax2 = ax1.twinx()

            x_axis = np.arange(price-STD_WIDTH*std, price+STD_WIDTH*std, 0.1) 

            ax2.plot(x_axis, norm.pdf(x_axis, price, std), color='r')
            ax2.set_ylabel('probability', color='r')
            ax2.tick_params(axis='y', labelcolor='r')

            fig.tight_layout()
        plt.show()
    
    @staticmethod
    def getStrikeNearPrice(strikes: list, price: float):
        for i in range(len(strikes)):
            if strikes[i] != None and strikes[i] > price:
                return strikes[i], i
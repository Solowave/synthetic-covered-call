import numpy as np
from .portfolio import Portfolio

class MonteCarloSimulation:
    def __init__(self, portfolio: Portfolio, trials: int, steps: int, price: float, volatility: float, funds: float):
        self.start_price = price
        self.volatility = volatility
        self.steps = steps
        self.funds = funds
        self.trials = trials
        self.portfolio = portfolio

        self.current_price = self.start_price
        self.price_history = [self.current_price]
        self.funds_history = [self.funds]

    def getMaxDrawdown(self, cash_allocation: float, option_allocation: float, daily_interest_rate = .000137):
        if(cash_allocation + option_allocation != 1):
            raise Exception("Cash and Option Allocation must be equal than 1")
        interest = (cash_allocation * self.funds) * self.steps * daily_interest_rate

        allocation = option_allocation * self.funds
        option_returns = self.portfolio.getReturn(0, allocation)
        
        self.current_price = self.start_price
        self.price_history = [self.current_price]

        result = (option_returns + interest) / self.funds
        
        return max(-1, result)

    def simulate(self, cash_allocation: float, option_allocation: float, daily_interest_rate = .000137):
        results = []

        for _ in range(self.trials):
            if(cash_allocation + option_allocation != 1):
                raise Exception("Cash and Option Allocation must be equal than 1")
            
            interest = (cash_allocation * self.funds) * self.steps * daily_interest_rate

            for _ in range(self.steps):
                # TODO: Replace with sampling
                new_price = self.current_price + np.random.normal(0, self.volatility)
                
                self.current_price = new_price
                self.price_history.append(new_price)
            
            allocation = option_allocation * self.funds
            option_returns = self.portfolio.getReturn(self.current_price, allocation)

            result = option_returns + interest

            results.append(result)

            # Reset variables
            self.current_price = self.start_price
            self.price_history = [self.current_price]
        
        return (np.mean(results), np.std(results))
    
    def simulateOnce(self, cash_allocation: float, option_allocation: float, daily_interest_rate = .000137):
        results = []

        if(cash_allocation + option_allocation != 1):
            raise Exception("Cash and Option Allocation must be equal than 1")
        
        interest = (cash_allocation * self.funds) * self.steps * daily_interest_rate

        for _ in range(self.steps):
            new_price = self.current_price + np.random.normal(0, self.volatility)
            self.current_price = new_price
            self.price_history.append(new_price)
        
            allocation = option_allocation * self.funds
            option_returns = self.portfolio.getReturn(self.current_price, allocation)

            result = option_returns + interest

            results.append(result)
        
        return (result, np.std(results))
         
    def run(self, cash_allocation: float, option_allocation: float, daily_interest_rate = .000137, display: bool = False):
        if(cash_allocation + option_allocation != 1):
            raise Exception("Cash and Option Allocation must be equal than 1")
        interest = (cash_allocation * self.funds) * self.steps * daily_interest_rate

        for tick in range(self.steps):
            new_price = self.current_price + np.random.normal(0, self.volatility)
            self.current_price = new_price
            self.price_history.append(new_price)
        
        allocation = option_allocation * self.funds
        option_returns = self.portfolio.getReturn(self.current_price, allocation)

        worst_result = np.min(self.price_history)
        max_drawdowm = self.portfolio.getReturn(worst_result, allocation)

        result = option_returns + interest

        return (result, max_drawdowm)
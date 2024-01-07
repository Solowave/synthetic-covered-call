# Background

[Yieldmax](https://www.yieldmaxetfs.com/our-etfs/) is a company that hosts a collection of ETF's that trade Synthetic Covered Calls on popular stocks in attempts to capture monthly income through these option premiums.

# Data

All Stock and Options data derived from [Tradier](https://www.tradier.com).

# Strategy

![image info](./output.png)
Market Data from 1/6/2024 at 1:14pm.

Strikes were as follows:
- Long Call ATM:  240.0
- Short Put ATM:  240.0
- Short Call OTM:  265.0

Current price of TSLA - $237.49

# Simulation

![image info](./simulation.png)
Shows Monte Carlo Simulation of TSLA stock over time period while option contract is active. From 1/6/2024 to 4/19/2024, or a little more than 70 trading days.

# Results
![image info](./allocations.png)
This image shows the results of different allocations of a cash balance ($100,000) where the option allocation is between (0, 100)% and the rest is cash which returned an interest at the current rate ~5.25%.

The strategy appears to have a weak positive relationship between option allocation and returns, even when accounting for the 5.25% interest paid on cash.

Best Fit Line data:
```
Slope: 0.31616203507715607
Intercept: -0.03168971855652475
R-value: 0.458842637103749
P-value: 1.5769465133709017e-06
Standard error: 0.06184419248624469
```

![image info](./results.png)

Since the strategy is a synthetic covered call, and as showed before there is exposed downside risk, the larger the balance that is put into the strategy, the higher the liklihood of a catastrophic drawdown.

Though the strategy can work in the short term, due to the exposed downside risk, it is important to keep in mind the risk of losing a sizable portion of the portfolio.

Therefore, similar to yieldmaxes trading strategy, it makes sense to only allocation a small portion of a trading balance to minimize the possibility liquidation.

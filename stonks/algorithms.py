#!/usr/bin/env python
## Trading bot algorithms
import sys
if sys.version_info[0] != 3 or sys.version_info[1] < 6:
  print("This script requires Python version >=3.6")
  sys.exit(1)

import decimal
import exchange

KIPPfastDays = 1
KIPPslowDays = 5

## Sell stocks when their fast (1 day) average crosses below their slow (5
#  day) average. Buy stocks when the fast average crosses above their slow
#  average, distribute cash based on steepness of crossing
#  @param symbols list of symbols to analyze
#  @param portfolio to purchase
def KIPP(symbols, portfolio):
  pairs = []
  totalMetric = 0
  for name in symbols:
    avgFast = 0
    if exchange.priceHistory(name, KIPPslowDays, time="close") is None:
      continue
    for i in range(1, KIPPfastDays + 1):
      avgFast += exchange.priceHistory(name, i, time="close")
      avgFast += exchange.priceHistory(name, i, time="open")
    avgFast = avgFast / KIPPfastDays

    avgSlow = 0
    for i in range(1, KIPPslowDays + 1):
      avgSlow += exchange.priceHistory(name, i, time="close")
      avgSlow += exchange.priceHistory(name, i, time="open")
    avgSlow = avgSlow / KIPPslowDays

    metric = avgFast / avgSlow - 1
    if metric < 0 and portfolio.shares(name) > 0:
      portfolio.sell(name, portfolio.shares(name))
    if metric > 0 and portfolio.shares(name) == 0:
      pairs.append((name, metric))
      totalMetric += metric
  for pair in pairs:
    toBuy = portfolio.cash * pair[1] / totalMetric
    quantity = toBuy / exchange.price(pair[0]) / 2
    portfolio.buy(pair[0], quantity)

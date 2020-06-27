#!/usr/bin/env python
## Trading bot algorithms
import sys
if sys.version_info[0] != 3 or sys.version_info[1] < 6:
  print("This script requires Python version >=3.6")
  sys.exit(1)

import decimal
import exchange

VGerSellFactor = 30
VGerHistoryDays = 30
KIPPfastDays = 1
KIPPslowDays = VGerHistoryDays

## Sell stocks when their fast (1 day) average crosses below their slow (5
#  day) average. Buy stocks when the fast average crosses above their slow
#  average, distribute cash based on steepness of crossing
#  @param symbols list of symbols to analyze
#  @param portfolio to purchase
def KIPP(symbols, portfolio):
  pairs = []
  for name in symbols:
    metric = 0
    if exchange.priceHistory(name, VGerHistoryDays - 1, time="close") is None:
      continue
    for i in range(1, VGerHistoryDays):
      dayChange = exchange.priceHistory(
        name, i, time="close") / exchange.priceHistory(name, i, time="open") - 1
      metric += dayChange
    pairs.append((name, metric))
  pairs.sort(key=lambda x: -x[1])
  for pair in pairs:
    quantity = decimal.Decimal(
      portfolio.value() / VGerSellFactor) / exchange.price(pair[0])
    if portfolio.sell(pair[0], quantity) != 0:
      break

  pairs.reverse()
  for pair in pairs:
    quantity = portfolio.cash / exchange.price(pair[0]) / 2
    if portfolio.buy(pair[0], quantity) != 0:
      break

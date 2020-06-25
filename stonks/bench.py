#!/usr/bin/env python
## Benchmark an algorithm over random initial conditions
import sys
if sys.version_info[0] != 3 or sys.version_info[1] < 6:
  print("This script requires Python version >=3.6")
  sys.exit(1)

import algorithms
import datetime
import exchange
import portfolio
import math
from matplotlib import dates
from matplotlib import pyplot
import mplfinance
import numpy
import pandas
import random
import scipy.stats as st

## Main function
def main():
  with open("symbolsPruned", "r", newline="\n") as file:
    symbols = file.read().strip().split("\n")

  percentages = []
  exchange.init(symbols, period=500, historyDays=algorithms.KIPPslowDays)
  for run in range(500):
    # Select a set of 5 random symbols from the entire set
    selectedSymbols = random.sample(symbols, 10)
    # print(selectedSymbols)

    period = random.randint(30, 500)
    exchange.reset(period)
    p = portfolio.Portfolio(3000)

    for i in range(period):
      if (i % 5) == 0:
        p.fund(150)

      exchange.openMarket()

      algorithms.KIPP(selectedSymbols, p)
      value = p.value()
      exchange.closeMarket()

    closeRatio = value / p.investment
    percentageYr = math.log(closeRatio) * 252 / period
    percentages.append(percentageYr * 100)
    print("{:3} ended with gain of ${:10.2f} with ${:10.2f} invested at {:6.1f}% {:6.1f}%(yr)".format(
      run, value - p.investment, p.investment, (closeRatio - 1) * 100, percentageYr * 100))

  print(st.describe(percentages))

  pyplot.hist(percentages, density=True, bins=50)
  mn, mx = pyplot.xlim()
  kde_xs = numpy.linspace(mn, mx, 301)
  kde = st.gaussian_kde(percentages)
  pyplot.plot(kde_xs, kde.pdf(kde_xs))
  pyplot.xlabel("Percentage (yr)")
  pyplot.ylabel("Probability")
  pyplot.xlim(min(percentages), max(percentages))
  pyplot.show()


if __name__ == "__main__":
  main()

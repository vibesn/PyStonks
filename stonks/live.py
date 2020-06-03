#!/usr/bin/env python
## Test an algorithm in real life
import sys
if sys.version_info[0] != 3 or sys.version_info[1] < 6:
  print("This script requires Python version >=3.6")
  sys.exit(1)

import algorithms
import datetime
import exchange
import pandas_market_calendars as mcal
import portfolioLive

## Main function
def main():
  today = datetime.date.today()
  nyse = mcal.get_calendar('NYSE')
  if len(nyse.valid_days(start_date=today, end_date=today)) == 0:
    print("Markets are closed today")
    return

  with open("symbolsPruned", "r", newline="\n") as file:
    symbols = file.read().strip().split("\n")

  exchange.init(
      symbols,
      period=1,
      historyDays=algorithms.KIPPslowDays)
  p = portfolioLive.Portfolio()

  algorithms.KIPP(symbols, p)


if __name__ == "__main__":
  main()

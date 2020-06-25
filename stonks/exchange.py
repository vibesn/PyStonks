#!/usr/bin/env python
## Exchange market fetching current day prices
import sys
if sys.version_info[0] != 3 or sys.version_info[1] < 6:
  print("This script requires Python version >=3.6")
  sys.exit(1)

import asyncio
from alpha_vantage.async_support.timeseries import TimeSeries
from collections import deque
import datetime
import decimal
import re

history = {}
historyOffset = 0
data = {}
dates = []
isOpen = False
today = None
currentDay = 0

API_KEY = open("apikey").read()

## Initialize the exchange
#  @param symbols list to manage
#  @param period number of days to make available ~(start [period] days ago)
#  @param history number of historical days to make available=
#  @param quiet True will not print each loaded symbol, False will
def init(symbols, period=100, historyDays=20, quiet=False):
  global dates
  global historyOffset
  historyOffset = historyDays

  outputSize = "compact"
  if period > 100:
    outputSize = "full"

  loop = asyncio.get_event_loop()
  tasks = [initSymbol(symbol, outputSize) for symbol in symbols]
  group = asyncio.gather(*tasks)
  results = loop.run_until_complete(group)
  for result in results:
    symbolDates = deque()
    symbolData = deque()
    symbolHistory = deque()

    dataRemaining = period
    historyRemaining = period + historyDays

    for key in result[1].keys():
      day = result[1][key]
      if dataRemaining > 0:
        symbolData.appendleft(day)

        date = re.sub(r" \d+:\d+:\d+", "", key)
        date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        symbolDates.appendleft(date)

        dataRemaining -= 1
      if historyRemaining > 0:
        symbolHistory.appendleft(day)
        historyRemaining -= 1

    while dataRemaining > 0:
      symbolData.appendleft(None)
      dataRemaining -= 1

    while historyRemaining > 0:
      symbolHistory.appendleft(None)
      historyRemaining -= 1

    data[result[0]] = symbolData
    history[result[0]] = symbolHistory

    if len(symbolDates) > len(dates):
      dates = symbolDates

## Asynchronously get the daily history of a symbol
#  @param symbol to fetch
#  @param outputSize of data to fetch: compact=100, full=all
#  @return dictionary {date: OHLC data}
async def initSymbol(symbol, outputSize="compact"):
  ts = TimeSeries(key=API_KEY)
  data, _ = await ts.get_daily_adjusted(symbol, outputsize=outputSize)
  await ts.close()
  return (symbol, data)

## Reinitialize the exchange
#  @param period number of days to make available ~(start [period] days ago)
def reset(period):
  global currentDay
  global isOpen
  global today
  currentDay = len(dates) - period
  isOpen = False
  today = None


## Get current price of symbol
#  @param symbol name to fetch
#  @param quantity to multiply by
#  @param time to evaluate price at: current, open, high, low, close
def price(symbol, quantity=1, time="current"):
  if time == "current":
    if isOpen:
      time = "1. open"
    else:
      time = "4. close"
  elif time == "open":
    time = "1. open"
  elif time == "high":
    time = "2. high"
  elif time == "low":
    time = "3. low"
  elif time == "close":
    time = "4. close"
  if data[symbol][currentDay] is None:
    return None
  return decimal.Decimal(data[symbol][currentDay]
                         [time]) * decimal.Decimal(quantity)


## Get current price of symbol
#  @param symbol name to fetch
#  @param quantity to multiply by
#  @param daysAgo to evaluate price at
#  @param time to evaluate price at: current, open, high, low, close
def priceHistory(symbol, daysAgo=0, time="open"):
  if time == "current":
    if isOpen:
      time = "1. open"
    else:
      time = "4. close"
  elif time == "open":
    time = "1. open"
  elif time == "high":
    time = "2. high"
  elif time == "low":
    time = "3. low"
  elif time == "close":
    time = "4. close"
  if history[symbol][currentDay + historyOffset - daysAgo] is None:
    return None
  return decimal.Decimal(history[symbol][currentDay + historyOffset - daysAgo ][time])

## Open the exchange by setting the prices of the symbols to their opening
#  price (next day)
def openMarket():
  global isOpen
  if isOpen:
    closeMarket()

  global today
  today = dates[currentDay]
  isOpen = True

## Close the exchange by setting the prices of the symbols to their closing
#  price
def closeMarket():
  global isOpen
  global currentDay
  if not isOpen:
    openMarket()
  currentDay = currentDay + 1
  isOpen = False

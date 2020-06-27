#!/usr/bin/env python
## Interface to Alpaca API
import sys
if sys.version_info[0] != 3 or sys.version_info[1] < 6:
  print("This script requires Python version >=3.6")
  sys.exit(1)

import alpaca_trade_api
import os

## Get list of symbols from Alpaca watchlist and current positions
def getSymbols(api):
  watchlists = api.get_watchlists()
  watchlistID = None
  if len(watchlists) == 1:
    watchlistID = watchlists[0].id
  else:
    for watchlist in watchlists:
      if watchlist.name.lower() == "stonks list":
        watchlistID = watchlist.id
  if watchlistID is None:
    print("Could not find suitable watchlist, create one named 'Stonks List'")
    sys.exit(1)

  watchlist = api.get_watchlist(watchlistID)
  symbols = [asset["symbol"] for asset in watchlist.assets]

  # Also add symbols currently held
  for position in api.list_positions():
    if position.symbol not in symbols:
      symbols.append(position.symbol)
  return symbols

def setup(paper=True):
  base_url = 'https://paper-api.alpaca.markets'
  if not paper:
    base_url = "https://api.alpaca.markets"
  api = alpaca_trade_api.REST(
      os.getenv("ALPACA_API_KEY"),
      os.getenv("ALPACA_SECRET_KEY"),
      base_url,
      api_version='v2')

  return getSymbols(api)

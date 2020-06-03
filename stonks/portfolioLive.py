#!/usr/bin/env python
## Live portfolio of ticket shares and liquid cash
import sys
if sys.version_info[0] != 3 or sys.version_info[1] < 6:
  print("This script requires Python version >=3.6")
  sys.exit(1)

import decimal
import exchange
import math
import portfolio
import robin_stocks as r

## Main function
class Portfolio(portfolio.Portfolio):

  ## Initialization of portfolio
  def __init__(self):
    with open("robinhood", "r", newline="\n") as file:
      username, password = file.read().strip().split("\n")

    r.login(username=username, password=password)

    cash = float(r.load_account_profile("cash"))
    super().__init__(cash)

    holdings = r.build_holdings()
    for symbol in holdings.keys():
      holding = holdings[symbol]
      self.tickets[symbol] = float(holding["quantity"])

  ## Withdraw an amount of cash from the portfolio
  #  @param symbol to purchase
  #  @param quantity of shares to purchase
  #  @return real quantity bought
  def buy(self, symbol, quantity):
    quantity = super().buy(symbol, quantity, receipt=True)
    if quantity > 0:
      result = r.order_buy_market(symbol, quantity)
      print(result["state"])
    return quantity

  ## Deposit an amount of cash into the portfolio
  #  @param symbol to purchase
  #  @param quantity of shares to purchase
  #  @return real quantity sold
  def sell(self, symbol, quantity):
    quantity = super().sell(symbol, quantity, receipt=True)
    if quantity > 0:
      result = r.order_sell_market(symbol, quantity)
      print(result["state"])
    return quantity

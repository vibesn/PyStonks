#!/usr/bin/env python
## Portfolio of ticket shares and liquid cash
import sys
if sys.version_info[0] != 3 or sys.version_info[1] < 6:
  print("This script requires Python version >=3.6")
  sys.exit(1)

import decimal
import exchange
import math

## Main function
class Portfolio:

  ## Initialization of portfolio
  #  @param cash initial investment into the portfolio
  def __init__(self, cash):
    self.investment = float(cash)
    self.cash = decimal.Decimal(cash)
    self.tickets = {}

  ## String representation
  #  @param self object pointer
  #  @return value of portfolio: $xxxx.xx
  def __str__(self):
    return "${:6.2f}".format(self.value())

  ## Withdraw an amount of cash from the portfolio
  #  @param symbol to purchase
  #  @param quantity of shares to purchase
  #  @param receipt True will print out a receipt for the transaction
  #  @return real quantity bought
  def buy(self, symbol, quantity, receipt=False):
    quantity = math.floor(quantity)
    price = exchange.price(symbol, quantity)
    if price > self.cash:
      return 0
    self.cash -= price
    if symbol not in self.tickets:
      self.tickets[symbol] = 0
    self.tickets[symbol] += quantity
    if receipt:
      print("Buy  {:2} of {:5} for ${:5.2f}".format(quantity, symbol, price))
    return quantity

  ## Deposit an amount of cash into the portfolio
  #  @param symbol to purchase
  #  @param quantity of shares to purchase
  #  @param receipt True will print out a receipt for the transaction
  #  @return real quantity sold
  def sell(self, symbol, quantity, receipt=False):
    if symbol not in self.tickets:
      return 0
    quantity = math.floor(min(quantity, self.tickets[symbol]))
    price = exchange.price(symbol, quantity)
    self.cash += price
    self.tickets[symbol] -= quantity
    if receipt:
      print("Sell {:2} of {:5} for ${:5.2f}".format(quantity, symbol, price))
    return quantity

  ## Evaluate the portfolio: cash + shares
  #  @param time to evaluate price at: current, open, high, low, close
  #  @return value of portfolio
  def value(self, time="current"):
    value = self.cash
    for symbol in self.tickets.keys():
      value += exchange.price(symbol, self.tickets[symbol], time=time)
    return float(value)

  ## Get the number of shares of the symbol
  #  @param symbol to inquire
  #  @return number of shares
  def shares(self, symbol):
    if symbol not in self.tickets:
      return 0
    return self.tickets[symbol]

  ## Fund the algorithm with more cash
  #  @param cash amount to fund
  def fund(self, cash):
    self.cash += decimal.Decimal(cash)
    self.investment += float(cash)

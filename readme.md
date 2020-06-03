# Stonks: Algorithmic Trading #
An algorithmic trading project for testing and benchmarking robots and operating robots on live finances
* AlphaVantage API
* Robinhood broker API

## Prerequisites ##
* [Python 3.6+](https://www.python.org/downloads/)
* python packages
  * matplotlib
  * mplfinance
  * numpy
  * pandas
  * scipy
  * alpha_vantage
  * pandas_market_calendars
  * robin_stocks

## Running ##
1. Create a list of symbols to trade with: `symbolsAll`, see `symbolsExample`
2. Get an API ket from [AlphaVantage](https://www.alphavantage.co/). Write to file `apikey`
3. Run pruner to evaluate the predicted health of the symbols: `python stonks prune`
4. Run tester to validate robot trades successfully: `python stonks test`
5. Run benchmark to give the robot random scenarios: `python stonks bench`
6. Add robinhood credentials to `robinhood`, see `robinhoodExample`
7. Give the robot control of your live account: `python stonks live`

## Adapting
The algorithms are located in `stonks\algorithms`. KIPP is a crossover robot that anaylzes a fast (1 day) average versus a slow (5 day) average. When those averages cross, it trades appropriately. Modify this function to create new robots. Symbols is the list of available stocks. Portfolio is the account of shares and cash. Exchange provides current and historical data: open, high, low, close

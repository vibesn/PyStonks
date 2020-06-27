# Stonks: Algorithmic Trading #
An algorithmic trading project for testing and benchmarking robots and operating robots on live finances
* Alpaca broker API
* Backtrader

## Prerequisites ##
* [Python 3.6+](https://www.python.org/downloads/)
* python packages
  * alpaca-backtrader-api
  * pandas

## Running ##
1. Create an account with [Alpaca](https://www.alpaca.markets)
2. Set environment variables `APCA_API_KEY_ID` and `APCA_API_SECRET_KEY` with provided credentials
3. Run tester to validate robot trades successfully: `python stonks test`
4. Run benchmark to give the robot random scenarios: `python stonks bench`
5. Give the robot control of your live account: `python stonks live`

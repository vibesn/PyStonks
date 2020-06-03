#!/usr/bin/env python
## Analyze and remove symbols that do not look profitable
import sys
if sys.version_info[0] != 3 or sys.version_info[1] < 6:
  print("This script requires Python version >=3.6")
  sys.exit(1)

import time
import exchange

## Main function
def main():
  with open("symbolsAll", "r", newline="\n") as file:
    symbols = file.read().strip().split("\n")

  exchange.init(symbols)

  prunedSymbols = []
  for name in symbols:
    data = exchange.data[name]
    percent = float(data[-1]["4. close"]) / float(data[0]["4. close"]) - 1
    if percent > 0:
      print("Kept    {:5}, 100 day percentage {:3.2f}%".format(
          name, percent * 100))
      prunedSymbols.append((name, percent))
    else:
      print("Pruning {:5}, 100 day percentage {:3.2f}%".format(
          name, percent * 100))

  prunedSymbols.sort(key=lambda x: -x[1])
  # prunedSymbols = prunedSymbols[:30]

  with open("symbolsPruned", "w", newline="\n") as file:
    file.write("\n".join([symbol[0] for symbol in prunedSymbols]))


if __name__ == "__main__":
  main()

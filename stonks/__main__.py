#!/usr/bin/env python
## Trading bot programs
import sys
if sys.version_info[0] != 3 or sys.version_info[1] < 6:
  print("This script requires Python version >=3.6")
  sys.exit(1)

import bench
import live
import prune
import test

if __name__ == "__main__":
  if len(sys.argv) < 2:
    mode = None
  else:
    mode = sys.argv[1].lower()

  if mode == "test":
    print("Testing")
    test.main()
  elif mode == "bench":
    print("Benchmarking")
    bench.main()
  elif mode == "prune":
    print("Pruning symbols")
    prune.main()
  elif mode == "live":
    print("Live Trading")
    live.main()
  else:
    print("Perform or test a stock trading algorithm")
    print("Follow with mode to execute algorithm")
    print("\"test\": test an algorithm over longest history period as possible")
    print("\"bench\": benchmark an algorithm over combination of symbols")
    print("\"prune\": prune the list of symbols to only likely profitable ones")
    print("\"live\": run an algorithm with live trading")

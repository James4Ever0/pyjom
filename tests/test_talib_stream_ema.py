import talib
from talib import stream
import numpy as np

# check the difference
import timeit

close = np.random.random(100)
print(close.dtype)
breakpoint()
# close = np.append(close,10)
close = np.append(close[1:], 10)
mtime = timeit.timeit(lambda: np.append(close, 10), number=1)  # why so many times?

# the Function API

# really don't know which is faster.

output = timeit.timeit(
    lambda: talib.SMA(close), number=1
)  # why you take it so damn long?
# the Streaming API
latest = timeit.timeit(lambda: stream.SMA(close[-20:]), number=1)

print(output)
print(latest)
print(close)
print(mtime)  # why taking so long?

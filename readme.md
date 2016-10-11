# pyxorshift

Implements a simple PRNG using the xorshift algorithm.

Depends on numpy.

``` python
from xorshift import xorshift
rng = xorshift()
# Get a random integer in the range 0 (inclusive) to 10 (exclusive)
print rng.next_int(0, 10)
# Get a random floating point number in the range 0.0 (inclusive) to 10.0 (inclusive)
print rng.next_float(0.0, 10.0)
```

The above program will print the same sequence of numbers every time because the seeds are preset and constant.

For almost all most use cases, you will want to select a seed other than the default. System time is a good source of entropy for this.

``` python
from xorshift import xorshift
from time import time
rng = xorshift(int(time * 1000))
print rng.next_int(0, 10)
```

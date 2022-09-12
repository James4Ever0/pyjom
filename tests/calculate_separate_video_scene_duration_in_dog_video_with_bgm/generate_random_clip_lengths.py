std, mean = 1.6674874515595588, 2.839698412698412
# using gaussian distribution
# accepting both mean and standard deviation

nMin, nMax = 0.6, 7.833
# while you need to make sure the value is in bound.

import random

inBound = lambda number: min(nMax, max(nMin, number))
randomFunction = lambda: random.gauss(mean, std)

for _ in range(30):
    print(randomFunction())
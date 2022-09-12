std, mean = 1.6674874515595588, 2.839698412698412
scale, loc = std, mean
# using gaussian distribution
# accepting both mean and standard deviation
# this is truncated gaussian, not just normal distribution

myclip_a, myclip_b = 0.6, 7.833
# while you need to make sure the value is in bound.

# import random
from scipy.stats import truncnorm

a, b = (myclip_a - loc) / scale, (myclip_b - loc) / scale

randVar = truncnorm(a,b)
randomFunction = lambda: randVar.rvs(1)[0]*scale+loc
# inBound = lambda number: min(nMax, max(nMin, number))
# randomFunction = lambda: inBound(random.gauss(mean, std))

for _ in range(30):
    print(randomFunction())
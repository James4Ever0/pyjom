# not overriding math.
# do some ranged stuff here...
def ():
    import sympy

# make sure every subset is ordered.
mSet = [(1.0,1.1,1.2),(2.4,2.5,2.6)]
mSet2 = [(0.9,1.05,1.15),(2.45,2.55,2.65,2.75)]

# convert to intervals first please?
mSetIntervals = [(x[0],x[-1]) for x in mSet]
mSet2Intervals = [(x[0],x[-1]) for x in mSet2]

# additional check: these intervals cannot overlap!
def checkOverlap(intervalTupleList):
  unionInterval = sympy.EmptySet # shall be empty here.
  for start, end in intervalTupleList:
    newInterval = sympy.Interval(start,end)
    isOverlapped = (sympy.EmptySet == unionInterval.intersect(newInterval))
    if isOverlapped:
      print("INTERVAL", newInterval, "OVERLAPPED!")
      return isOverlapped
    unionInterval += newInterval
  return False

assert not checkOverlap(mSetIntervals)
assert not checkOverlap(mSet2Intervals)
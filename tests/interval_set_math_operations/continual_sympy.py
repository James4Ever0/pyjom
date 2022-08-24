#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sympy

def unionToTupleList(myUnion):
  unionBoundaries = list(myUnion.boundary)
  leftBoundaries = unionBoundaries[::2]
  rightBoundaries = unionBoundaries[1::2]
  return list(zip(leftBoundaries, rightBoundaries))

def tupleSetToUncertain(mSet):
  for start, end in mSet:
    if mUncertain is None:
      mUncertain = sympy.Interval(start,end)
    else:
      mUncertain += sympy.Interval(start,end)
  typeUncertain = type(mUncertain)
  return mUncertain, typeUncertain

# borrowed from above code.
def mergeOverlappedInIntervalTupleList(intervalTupleList):
  mUncertain, _ = tupleSetToUncertain(intervalTupleList)
  mUncertainBoundaryList = list(mUncertain.boundary)
  mergedIntervalTupleList = zip(mUncertainBoundaryList[::2], mUncertainBoundaryList[1::2])
  return mergedIntervalTupleList

mSet = [(0,1), (2,3)]
mUncertain, typeUncertain = tupleSetToUncertain(mSet)
unrolledMSet = list(mUncertain.boundary)
# can be either sympy.sets.sets.Interval of sympy.sets.sets.Union

mSet2 = [(0.5,1.5),(1.6,2.5)]
mUncertain2, typeUncertain2 = tupleSetToUncertain(mSet2)
unrolledMSet2 = list(mUncertain2.boundary)


*

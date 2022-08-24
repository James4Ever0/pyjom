#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sympy

def unionToTupleList(myUnion):
  #  seriously wrong. this will fuck up.
  unionBoundaries = list(myUnion.boundary)
  unionBoundaries.sort()
  leftBoundaries = unionBoundaries[::2]
  rightBoundaries = unionBoundaries[1::2]
  return list(zip(leftBoundaries, rightBoundaries))

def tupleSetToUncertain(mSet):
  mUncertain = None
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
  mUncertainBoundaryList.sort()
  #  print(mUncertain)
  #  print(mUncertainBoundaryList)
  mergedIntervalTupleList = list(zip(mUncertainBoundaryList[::2], mUncertainBoundaryList[1::2]))
  # print(mergedIntervalTupleList)
  return mergedIntervalTupleList

mSet = [(0,1), (2,3)]
mUncertain, typeUncertain = tupleSetToUncertain(mSet)
unrolledMSet = list(mUncertain.boundary)
# can be either sympy.sets.sets.Interval of sympy.sets.sets.Union

mSet2 = [(0.5,1.5),(1.6,2.5)]
mUncertain2, typeUncertain2 = tupleSetToUncertain(mSet2)
unrolledMSet2 = list(mUncertain2.boundary)

print("MSET", mSet)
print("MSET2", mSet2)

############################################################

# hypothetical mSet2 and mUncertain2! please complete the hypothetical shit and make it runnable!

def checkCommon(subInterval, masterInterval):
  return subInterval == sympy.Intersection(subInterval, masterInterval)

mUncertains = [mUncertain, mUncertain2]
subIntervals = list(set(unrolledMSet2 + unrolledMSet))
subIntervals.sort()

subIntervals = zip(subIntervals[:-1], subIntervals[1:])
subIntervals = list(subIntervals)
#  breakpoint()
# for subIntervals, it's still not real interval but tuple at above line.

reversedCats = {}

import functools
subIntervalUnion = functools.reduce(lambda a,b: a+b, mUncertains)

for subIntervalIndex, (start, end) in enumerate(subIntervals):
  subIntervalCandidate = sympy.Interval(start, end)

  reverseIndex = [] # there must be at least one such index.
  for index, uncertainCandidate in enumerate(mUncertains):
    if checkCommon(subIntervalCandidate, uncertainCandidate):
      reverseIndex.append(index) # this is the index of the in-common set of the original set list
  reversedCats.update({subIntervalIndex:reverseIndex}) # need to sort and index? or not to sort because this is already done?

normalCats = {}
for k,v in reversedCats.items():
  v.sort()
  v = tuple(v)
  normalCats.update({v:normalCats.get(v, [])+[k]})
# we only get interval, not the actural union period!
# how to get interval elements out of union structure for hell sake?

finalCats = {}
for k,v in normalCats.items():
  # now k is the original set index list, representing belonging of the below union.
  #  print(subIntervals)
  #  print(index)
  #  print(v)
  #  breakpoint()
  mFinalUnionCandidate = [subIntervals[index] for index in v]

  ## REPLACED ##
  # mFinalUnionCandidate, _ = tupleSetToUncertain(mFinalUnionCandidate)

  ##### union to tuple list, could be replaced #####
  #mFinalUnionCandidateBoundaryList = list(mFinalUnionCandidate.boundary)
  #left_bounds, right_bounds = mFinalUnionCandidateBoundaryList[0::2],mFinalUnionCandidateBoundaryList[1::2] # check it dammit! not sure how to step the list properly?
  #mFinalIntervalListCandidate = list(zip(left_bounds, right_bounds))

  # mFinalIntervalListCandidate = unionToTupleList(mFinalUnionCandidate)
  ##### union to tuple list, could be replaced #####
  ## REPLACED ##
  # print("M_FINAL_UNION_CANDIDATE",mFinalUnionCandidate)

  mFinalIntervalListCandidate = mergeOverlappedInIntervalTupleList(mFinalUnionCandidate)
  # print("M_FINAL_INTERVAL_LIST_CANDIDATE", mFinalIntervalListCandidate)

  # breakpoint()
  finalCats.update({k:mFinalIntervalListCandidate.copy()})
# this whole calculation could just be exponential. goddamn it?
# before that, we need to get the "empty" out. but is that really necessary? i think it is, as an important feature.
#  subIntervalsStart, subIntervalsEnd = subIntervals[0][0], subIntervals[-1][-1]
#
#  relativeCompleteInterval = sympy.Interval(subIntervalsStart, subIntervalsEnd)
#
# subIntervalUnion
#  emptyIntervalUnion = relativeCompleteInterval - subIntervalUnion # really uncertain if it is just a union or not.
#  emptyIntervalTupleList = unionToTupleList(emptyIntervalUnion)
#
#  finalCats.update({"empty":emptyIntervalTupleList})
finalCats.update({"empty":finalCats[()]})
del finalCats[()]

print("_____FINAL CATS_____")
print(finalCats)

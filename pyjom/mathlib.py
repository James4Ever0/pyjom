# not overriding math.
# do some ranged stuff here...

from pykalman import KalmanFilter
import numpy as np

def uniq(mList, ordered=True, random=False):
    if ordered:

    else:
        result = list(set(mList))

def get1DArrayEMA(mArray, N=5):
    weights = np.exp(np.linspace(0, 1, N))
    weights = weights / np.sum(weights)
    ema = np.convolve(weights, mArray, mode="valid")
    return ema
    
def Kalman1D(observations, damping=0.2):
    # To return the smoothed time series data
    observation_covariance = damping
    initial_value_guess = observations[0]
    transition_matrix = 1
    transition_covariance = 0.1
    initial_value_guess
    kf = KalmanFilter(
        initial_state_mean=initial_value_guess,
        initial_state_covariance=observation_covariance,
        observation_covariance=observation_covariance,
        transition_covariance=transition_covariance,
        transition_matrices=transition_matrix,
    )
    pred_state, state_cov = kf.smooth(observations)
    return pred_state
def getContinualNonSympyMergeResult(inputMSetCandidates):
    # basically the same example.
    # assume no overlapping here.
    import sympy

    def unionToTupleList(myUnion):
        unionBoundaries = list(myUnion.boundary)
        unionBoundaries.sort()
        leftBoundaries = unionBoundaries[::2]
        rightBoundaries = unionBoundaries[1::2]
        return list(zip(leftBoundaries, rightBoundaries))

    def tupleSetToUncertain(mSet):
        mUncertain = None
        for start, end in mSet:
            if mUncertain is None:
                mUncertain = sympy.Interval(start, end)
            else:
                mUncertain += sympy.Interval(start, end)
        typeUncertain = type(mUncertain)
        return mUncertain, typeUncertain

    def mergeOverlappedInIntervalTupleList(intervalTupleList):
        mUncertain, _ = tupleSetToUncertain(intervalTupleList)
        mUncertainBoundaryList = list(mUncertain.boundary)
        mUncertainBoundaryList.sort()
        mergedIntervalTupleList = list(
            zip(mUncertainBoundaryList[::2], mUncertainBoundaryList[1::2])
        )
        return mergedIntervalTupleList

    # mSet = mergeOverlappedInIntervalTupleList([(0, 1), (2, 3)])
    # mSet2 = mergeOverlappedInIntervalTupleList([(0.5, 1.5), (1.6, 2.5)])

    # print("MSET", mSet)
    # print("MSET2", mSet2)

    mSetCandidates = [
        mergeOverlappedInIntervalTupleList(x) for x in inputMSetCandidates
    ]
    mSetUnified = [x for y in mSetCandidates for x in y]
    leftBoundaryList = set([x[0] for x in mSetUnified])
    rightBoundaryList = set([x[1] for x in mSetUnified])
    # they may freaking overlap.
    # if want nearby-merge strategy, simply just expand all intervals, merge them with union and shrink the individual intervals inside union respectively.

    markers = {
        "enter": {k: [] for k in leftBoundaryList},
        "exit": {k: [] for k in rightBoundaryList},
    }

    for index, mSetCandidate in enumerate(mSetCandidates):
        leftBoundaryListOfCandidate = [x[0] for x in mSetCandidate]
        rightBoundaryListOfCandidate = [x[1] for x in mSetCandidate]
        for leftBoundaryOfCandidate in leftBoundaryListOfCandidate:
            markers["enter"][leftBoundaryOfCandidate].append(index)  # remap this thing!
        for rightBoundaryOfCandidate in rightBoundaryListOfCandidate:
            markers["exit"][rightBoundaryOfCandidate].append(index)  # remap this thing!

    # now, iterate through the boundaries of mSetUnified.
    unifiedBoundaryList = leftBoundaryList.union(
        rightBoundaryList
    )  # call me a set instead of a list please? now we must sort this thing
    unifiedBoundaryList = list(unifiedBoundaryList)
    unifiedBoundaryList.sort()

    unifiedBoundaryMarks = {}
    finalMappings = {}
    # print("MARKERS", markers)
    # breakpoint()
    for index, boundary in enumerate(unifiedBoundaryList):
        previousMark = unifiedBoundaryMarks.get(index - 1, [])
        enterList = markers["enter"].get(boundary, [])
        exitList = markers["exit"].get(boundary, [])
        currentMark = set(previousMark + enterList).difference(set(exitList))
        currentMark = list(currentMark)
        unifiedBoundaryMarks.update({index: currentMark})
        # now, handle the change? or not?
        # let's just deal those empty ones, shall we?
        if previousMark == []:  # inside it is empty range.
            # elif currentMark == []:
            if index == 0:
                continue  # just the start, no need to note this down.
            else:
                finalMappings.update(
                    {
                        "empty": finalMappings.get("empty", [])
                        + [(unifiedBoundaryList[index - 1], boundary)]
                    }
                )
            # the end of previous mark! this interval belongs to previousMark
        else:
            key = previousMark.copy()
            key.sort()
            key = tuple(key)
            finalMappings.update(
                {
                    key: finalMappings.get(key, [])
                    + [(unifiedBoundaryList[index - 1], boundary)]
                }
            )
            # also the end of previous mark! belongs to previousMark.

    ### NOW THE FINAL OUTPUT ###
    finalCats = {}
    for key, value in finalMappings.items():
        # value is an array containing subInterval tuples.
        value = mergeOverlappedInIntervalTupleList(value)
        finalCats.update({key: value})

    # print("______________FINAL CATS______________")
    # print(finalCats)
    return finalCats


def getContinualMappedNonSympyMergeResult(mRangesDict, concatSymbol="|", noEmpty=True):
    mKeyMaps = list(mRangesDict.keys())
    mSetCandidates = [mRangesDict[key] for key in mKeyMaps]
    # the next step will automatically merge all overlapped candidates.
    finalCats = getContinualNonSympyMergeResult(mSetCandidates)
    finalCatsMapped = {
        concatSymbol.join([mKeyMaps[k] for k in mTuple]): finalCats[mTuple]
        for mTuple in finalCats.keys()
        if type(mTuple) == tuple
    }
    if not noEmpty:
        finalCatsMapped.update(
            {k: finalCats[k] for k in finalCats.keys() if type(k) != tuple}
        )
    return finalCatsMapped
    # default not to output empty set?


def getContinualMappedNonSympyMergeResultWithRangedEmpty(
    mRangesDict, start, end, concatSymbol="|"
):
    import uuid

    emptySetName = str(uuid.uuid4())
    newRangesDict = mRangesDict.copy()
    newRangesDict.update({emptySetName: [(start, end)]})
    newRangesDict = getContinualMappedNonSympyMergeResult(
        newRangesDict, concatSymbol="|", noEmpty=True
    )
    newRangesDict = {
        key: [
            (mStart, mEnd)
            for mStart, mEnd in newRangesDict[key]
            if mStart >= start and mEnd <= end
        ]
        for key in newRangesDict.keys()
    }
    newRangesDict = {
        key: newRangesDict[key]
        for key in newRangesDict.keys()
        if newRangesDict[key] != []
    }
    finalNewRangesDict = {}
    for key in newRangesDict.keys():
        mergedEmptySetName = "{}{}".format(concatSymbol, emptySetName)
        if mergedEmptySetName in key:
            newKey = key.replace(mergedEmptySetName,"")
            finalNewRangesDict.update({newKey:newRangesDict[key]})
        elif key == emptySetName:
            finalNewRangesDict.update({'empty':newRangesDict[key]})
        else:
            finalNewRangesDict.update({key:newRangesDict[key]})
    return finalNewRangesDict

def mergedRangesToSequential(renderDict):
    renderList = []
    for renderCommandString in renderDict.keys():
        commandTimeSpans = renderDict[renderCommandString].copy()
        # commandTimeSpan.sort(key=lambda x: x[0])
        for commandTimeSpan in commandTimeSpans:
            renderList.append([renderCommandString, commandTimeSpan].copy())
    renderList.sort(key=lambda x: x[1][0])
    return renderList
    # for renderCommandString, commandTimeSpan in renderList:
    #     print(renderCommandString, commandTimeSpan)

def sequentialToMergedRanges(sequence):
    mergedRanges = {}
    for commandString, commandTimeSpan in sequence:
        mergedRanges.update({commandString: mergedRanges.get(commandString,[])+[commandTimeSpan]})
    mergedRanges = getContinualMappedNonSympyMergeResult(mergedRanges)
    return mergedRanges
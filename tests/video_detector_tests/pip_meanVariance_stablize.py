from mathlib import *

# from ...pyjom.mathlib import sequentialToMergedRanges

# you can use yolo to train network to detect these sharp corners, total four sharp corners.

# but it might fail to do so.

# but what about other stuff?
# whatever let's just use this.


def sampledStablePipRegionExporter(data, defaultWidth, defaultHeight):
    defaultWidth, defaultHeight = int(defaultWidth), int(defaultHeight)
    import numpy as np

    data = np.array(data)

    def getAlikeValueMerged(mArray, threshold=35):
        for index, elem in enumerate(mArray[:-1]):
            nextElem = mArray[index + 1]
            if abs(nextElem - elem) < threshold:
                mArray[index + 1] = elem
        return mArray

    def listToRangedDictWithLabel(mList, label):
        resultDict = {}
        for index, elem in enumerate(mList):
            mKey = "{}:{}".format(label, int(elem))
            resultDict.update({mKey: resultDict.get(mKey, []) + [(index, index + 1)]})
        return resultDict
    
    def get1DArrayEMA(mArray,N=5):
        weights=np.exp(np.linspace(0,1,N))
        weights =weights/np.sum(weights)
        ema = np.convolve(weights, mArray, mode='valid')
        return ema

    def pointsToRangedDictWithLabel(mArray, label, threshold=35):
        mArray = get1DArrayEMA(mArray)
        mArray = getAlikeValueMerged(mArray, threshold=threshold)
        return listToRangedDictWithLabel(mArray, label)
    threshold = int(max(defaultWidth, defaultHeight)*0.02734375)
    xLeftPoints = pointsToRangedDictWithLabel(data[:, 0, 0], "xleft", threshold = threshold)
    yLeftPoints = pointsToRangedDictWithLabel(data[:, 0, 1], "yleft", threshold = threshold)
    xRightPoints = pointsToRangedDictWithLabel(data[:, 1, 0], "xright", threshold = threshold)
    yRightPoints = pointsToRangedDictWithLabel(data[:, 1, 1], "yright", threshold = threshold)

    commandDict = {}
    for mDict in [xLeftPoints, yLeftPoints, xRightPoints, yRightPoints]:
        commandDict.update(mDict)
    commandDict = getContinualMappedNonSympyMergeResult(commandDict)
    commandDictSequential = mergedRangesToSequential(commandDict)

    def getSpanDuration(span):
        start, end = span
        return end - start

    itemDurationThreshold = 10
    # framerate?

    while True:
        # print("LOOP COUNT:", loopCount)
        # loopCount+=1
        # noAlter = True
        beforeChange = [item[0] for item in commandDictSequential].copy()
        for i in range(len(commandDictSequential) - 1):
            currentItem = commandDictSequential[i]
            nextItem = commandDictSequential[i + 1]
            currentItemCommand = currentItem[0]
            currentItemDuration = getSpanDuration(currentItem[1])
            nextItemCommand = nextItem[0]
            nextItemDuration = getSpanDuration(nextItem[1])
            if currentItemDuration < itemDurationThreshold:
                if nextItemCommand != currentItemCommand and nextItemDuration >= itemDurationThreshold:
                    # print("HERE0",i, currentItemCommand, nextItemCommand)
                    commandDictSequential[i][0] = nextItemCommand
                    # noAlter=False
            if nextItemDuration < itemDurationThreshold:
                if nextItemCommand != currentItemCommand :
                    # print("HERE1",i, currentItemCommand, nextItemCommand)
                    commandDictSequential[i + 1][0] = currentItemCommand
                    # noAlter=False
        afterChange = [item[0] for item in commandDictSequential].copy()
        noAlter = beforeChange == afterChange
        if noAlter:
            break
    preFinalCommandDict = sequentialToMergedRanges(commandDictSequential)
    finalCommandDict = {}
    for key, elem in preFinalCommandDict.items():
        # print(key,elem)
        varNames = ["xleft", "yleft", "xright", "yright"]
        defaultValues = [0, 0, defaultWidth, defaultHeight]
        for varName, defaultValue in zip(varNames, defaultValues):
            key = key.replace(
                "{}:empty".format(varName), "{}:{}".format(varName, defaultValue)
            )
        # print(key,elem)
        # breakpoint()
        import parse

        formatString = (
            "xleft:{xleft:d}|yleft:{yleft:d}|xright:{xright:d}|yright:{yright:d}"
        )
        commandArguments = parse.parse(formatString, key)
        x, y, w, h = (
            commandArguments["xleft"],
            commandArguments["yleft"],
            commandArguments["xright"] - commandArguments["xleft"],
            commandArguments["yright"] - commandArguments["yleft"],
        )
        if w <= 0 or h <= 0:
            continue
        cropCommand = "crop_{}_{}_{}_{}".format(x, y, w, h)
        # print(cropCommand)
        finalCommandDict.update({cropCommand: elem})
        # print(elem)
        # the parser shall be in x,y,w,h with keywords.
        # we might want to parse the command string and reengineer this shit.
    return finalCommandDict


def kalmanStablePipRegionExporter(data, defaultWidth, defaultHeight):
    defaultWidth, defaultHeight = int(defaultWidth), int(defaultHeight)
    import numpy as np

    data = np.array(data)

    from pykalman import KalmanFilter

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

    def getSinglePointStableState(xLeftPoints, signalFilterThreshold=10, commandFloatMergeThreshold = 15, 
        stdThreshold = 1,
        slopeThreshold = 0.2):
        xLeftPointsFiltered = Kalman1D(xLeftPoints)
        xLeftPointsFiltered = xLeftPointsFiltered.reshape(-1)
        from itertools import groupby

        def extract_span(mlist, target=0):
            counter = 0
            spanList = []
            target_list = [(a, len(list(b))) for a, b in groupby(mlist)]
            for a, b in target_list:
                nextCounter = counter + b
                if a == target:
                    spanList.append((counter, nextCounter))
                counter = nextCounter
            return spanList

        # solve diff.
        xLeftPointsFilteredDiff = np.diff(xLeftPointsFiltered)
        # xLeftPointsFilteredDiff3 = np.diff(xLeftPointsFilteredDiff)
        # import matplotlib.pyplot as plt
        # plt.plot(xLeftPointsFilteredDiff)
        # plt.plot(xLeftPointsFiltered)
        # plt.plot(xLeftPoints)
        # plt.show()

        # xLeftPointsFilteredDiff3Filtered = Kalman1D(xLeftPointsFilteredDiff3)
        derivativeThreshold = 3
        # derivative3Threshold = 3
        xLeftPointsSignal = (
            (abs(xLeftPointsFilteredDiff) < derivativeThreshold)
            .astype(np.uint8)
            .tolist()
        )

        def signalFilter(signal, threshold=10):
            newSignal = np.zeros(len(signal))
            signalFiltered = extract_span(xLeftPointsSignal, target=1)
            newSignalRanges = []
            for start, end in signalFiltered:
                length = end - start
                if length >= threshold:
                    newSignalRanges.append((start, end))
                    newSignal[start : end + 1] = 1
            return newSignal, newSignalRanges

        xLeftPointsSignalFiltered, newSignalRanges = signalFilter(xLeftPointsSignal, threshold = signalFilterThreshold)
        xLeftPointsSignalFiltered *= 255

        mShrink = 2
        from sklearn.linear_model import LinearRegression

        target = []
        for start, end in newSignalRanges:
            # could we shrink the boundaries?
            mStart, mEnd = start + mShrink, end - mShrink
            if mEnd <= mStart:
                continue
            sample = xLeftPointsFiltered[mStart:mEnd]
            std = np.std(sample)
            if std > stdThreshold:
                continue
            model = LinearRegression()
            X, y = np.array(range(sample.shape[0])).reshape(-1, 1), sample
            model.fit(X, y)
            coef = model.coef_[0]  # careful!
            if abs(coef) > slopeThreshold:
                continue
            meanValue = int(np.mean(sample))
            target.append({"range": (start, end), "mean": meanValue})
            # print((start, end), std, coef)

        newTarget = {}

        for elem in target:
            meanStr = str(elem["mean"])
            mRange = elem["range"]
            newTarget.update({meanStr: newTarget.get(meanStr, []) + [mRange]})

        mStart = 0
        mEnd = len(xLeftPoints)
        newTarget = getContinualMappedNonSympyMergeResultWithRangedEmpty(
            newTarget, mStart, mEnd
        )
        newTargetSequential = mergedRangesToSequential(newTarget)

        if (newTargetSequential) == 1:
            if newTargetSequential[0][0] == "empty":
                # the whole thing is empty now. no need to investigate.
                print("NO STATIC PIP FOUND HERE.")
                return {}
        else:
            # newTargetSequential
            newTargetSequentialUpdated = []
            for index in range(len(newTargetSequential) - 1):
                elem = newTargetSequential[index]
                commandString, commandTimeSpan = elem
                nextElem = newTargetSequential[index + 1]
                nextCommandString, nextCommandTimeSpan = nextElem
                if commandString == "empty":
                    newTargetSequential[index][0] = nextCommandString
                else:
                    if nextCommandString == "empty":
                        newTargetSequential[index + 1][0] = commandString
                    else:  # compare the two!
                        commandFloat = float(commandString)
                        nextCommandFloat = float(nextCommandString)
                        if (
                            abs(commandFloat - nextCommandFloat)
                            < commandFloatMergeThreshold
                        ):
                            newTargetSequential[index + 1][0] = commandString
            # bring this sequential into dict again.
            answer = sequentialToMergedRanges(newTargetSequential)
            # print("_"*30, "ANSWER","_"*30)
            # for elem in answer.items():
            #     print(elem)
            return answer
        print("[FAILSAFE] SOMEHOW THE CODE SUCKS")
        return {}

    xLeftPoints = data[:, 0, 0]
    yLeftPoints = data[:, 0, 1]
    xRightPoints = data[:, 1, 0]
    yRightPoints = data[:, 1, 1]

    mPoints = [xLeftPoints, yLeftPoints, xRightPoints, yRightPoints]

    answers = []



    for mPoint in mPoints:
        answer = getSinglePointStableState(mPoint)
        answers.append(answer)
        # print("_"*30, "ANSWER","_"*30)
        # for elem in answer.items():
        #     print(elem)
    if answers == [{}, {}, {}, {}]:
        print("NO PIP FOUND")
        finalCommandDict = {}
    else:
        defaultCoord = [0, 0, defaultWidth, defaultHeight]  # deal with it later?
        defaults = [{str(defaultCoord[index]): [(0, len(data))]} for index in range(4)]
        for index in range(4):
            if answers[index] == {}:
                answers[index] = defaults[index]
        labels = ["xleft", "yleft", "xright", "yright"]
        commandDict = {}
        for index, elem in enumerate(answers):
            label = labels[index]
            newElem = {"{}:{}".format(label, key): elem[key] for key in elem.keys()}
            commandDict.update(newElem)
        commandDict = getContinualMappedNonSympyMergeResult(commandDict)
        commandDictSequential = mergedRangesToSequential(commandDict)

        def getSpanDuration(span):
            start, end = span
            return end - start

        itemDurationThreshold = 15
        # print("HERE")
        # loopCount = 0

        while True:
            # print("LOOP COUNT:", loopCount)
            # loopCount+=1
            # noAlter = True
            beforeChange = [item[0] for item in commandDictSequential].copy()
            for i in range(len(commandDictSequential) - 1):
                currentItem = commandDictSequential[i]
                nextItem = commandDictSequential[i + 1]
                currentItemCommand = currentItem[0]
                currentItemDuration = getSpanDuration(currentItem[1])
                nextItemCommand = nextItem[0]
                nextItemDuration = getSpanDuration(nextItem[1])
                if currentItemDuration < itemDurationThreshold:
                    if nextItemCommand != currentItemCommand:
                        # print("HERE0",i, currentItemCommand, nextItemCommand)
                        commandDictSequential[i][0] = nextItemCommand
                        # noAlter=False
                if nextItemDuration < itemDurationThreshold:
                    if nextItemCommand != currentItemCommand and currentItemDuration >= itemDurationThreshold:
                        # print("HERE1",i, currentItemCommand, nextItemCommand)
                        commandDictSequential[i + 1][0] = currentItemCommand
                        # noAlter=False
            afterChange = [item[0] for item in commandDictSequential].copy()
            noAlter = beforeChange == afterChange
            if noAlter:
                break
        preFinalCommandDict = sequentialToMergedRanges(commandDictSequential)
        finalCommandDict = {}
        for key, elem in preFinalCommandDict.items():
            # print(key,elem)
            varNames = ["xleft", "yleft", "xright", "yright"]
            defaultValues = [0, 0, defaultWidth, defaultHeight]
            for varName, defaultValue in zip(varNames, defaultValues):
                key = key.replace(
                    "{}:empty".format(varName), "{}:{}".format(varName, defaultValue)
                )
            # print(key,elem)
            # breakpoint()
            import parse

            formatString = (
                "xleft:{xleft:d}|yleft:{yleft:d}|xright:{xright:d}|yright:{yright:d}"
            )
            commandArguments = parse.parse(formatString, key)
            x, y, w, h = (
                commandArguments["xleft"],
                commandArguments["yleft"],
                commandArguments["xright"] - commandArguments["xleft"],
                commandArguments["yright"] - commandArguments["yleft"],
            )
            if w <= 0 or h <= 0:
                continue
            cropCommand = "crop_{}_{}_{}_{}".format(x, y, w, h)
            # print(cropCommand)
            finalCommandDict.update({cropCommand: elem})
            # print(elem)
            # the parser shall be in x,y,w,h with keywords.
            # we might want to parse the command string and reengineer this shit.
    return finalCommandDict


objective = "discrete"
# objective = "continual"
# objective = "continual_najie"

if __name__ == "__main__":
    # better plot this shit.
    import json

    if objective == "continual":
        dataDict = json.loads(open("pip_meanVariance.json", "r").read())
    elif objective == 'continual_najie':
        dataDict = json.loads(open("pip_meanVarianceSisterNa.json", "r").read())
    elif objective == "discrete":
        dataDict = json.loads(open("pip_discrete_meanVariance.json", "r").read())
    else:
        raise Exception("unknown objective: %s" % objective)
    # print(len(data)) # 589

    data = dataDict["data"]

    defaultWidth, defaultHeight = dataDict["width"], dataDict["height"]

    if objective in ["continual", 'continual_najie']:
        finalCommandDict = kalmanStablePipRegionExporter(
            data, defaultWidth, defaultHeight
        )
    else:
        finalCommandDict = sampledStablePipRegionExporter(
            data, defaultWidth, defaultHeight
        )

    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle

    fig, ax = plt.subplots()

    def plotRect(ax, x, y, width, height, facecolor):
        ax.add_patch(
            Rectangle((x, y), width, height, facecolor=facecolor, fill=True, alpha=0.5)
        )  # in 0-1

    ax.plot([[0, 0], [defaultWidth, defaultHeight]])
    plotRect(ax, 0, 0, defaultWidth, defaultHeight, "black")
    colors = ["red", "yellow", "blue",'orange','white','purple']
    for index, key in enumerate(finalCommandDict.keys()):
        import parse

        commandArguments = parse.parse("crop_{x:d}_{y:d}_{w:d}_{h:d}", key)
        color = colors[index%len(colors)]
        rect = [int(commandArguments[name]) for name in ["x", "y", "w", "h"]]
        print("RECT", rect, color, "SPAN", finalCommandDict[key])
        plotRect(ax, *rect, color)
    # breakpoint()
    plt.show()

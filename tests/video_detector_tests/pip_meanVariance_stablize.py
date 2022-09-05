import json
from mathlib import *

data = json.loads(open("pip_meanVariance.json",'r').read())

# print(len(data)) # 589
import numpy as np
data = np.array(data)
from pykalman import KalmanFilter

def Kalman1D(observations,damping=0.2):
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
            transition_matrices=transition_matrix
        )
    pred_state, state_cov = kf.smooth(observations)
    return pred_state

xLeftPoints = data[:,0,1]
xLeftPointsFiltered = Kalman1D(xLeftPoints)
xLeftPointsFiltered=xLeftPointsFiltered.reshape(-1)
from itertools import groupby
def extract_span(mlist, target=0):
    counter = 0
    spanList = []
    target_list = [(a,len(list(b))) for a,b in groupby(mlist)]
    for a,b in target_list:
        nextCounter = counter+b
        if a == target:
            spanList.append((counter, nextCounter))
        counter = nextCounter
    return spanList

# solve diff.
xLeftPointsFilteredDiff = np.diff(xLeftPointsFiltered)
# xLeftPointsFilteredDiff3 = np.diff(xLeftPointsFilteredDiff)

# xLeftPointsFilteredDiff3Filtered = Kalman1D(xLeftPointsFilteredDiff3)
derivativeThreshold = 3
# derivative3Threshold = 3
xLeftPointsSignal = (abs(xLeftPointsFilteredDiff) < derivativeThreshold).astype(np.uint8).tolist()

def signalFilter(signal, threshold = 10):
    newSignal = np.zeros(len(signal))
    signalFiltered = extract_span(xLeftPointsSignal, target=1)
    newSignalRanges = []
    for start, end in signalFiltered:
        length = end-start
        if length >= threshold:
            newSignalRanges.append((start, end))
            newSignal[start:end+1] = 1
    return newSignal, newSignalRanges

xLeftPointsSignalFiltered, newSignalRanges= signalFilter(xLeftPointsSignal)
xLeftPointsSignalFiltered *=255

mShrink = 2
from sklearn.linear_model import LinearRegression

stdThreshold = 1
slopeThreshold = 0.2
target = []
for start, end in newSignalRanges:
    # could we shrink the boundaries?
    mStart, mEnd = start+mShrink,end-mShrink
    if mEnd <= mStart: continue
    sample = xLeftPointsFiltered[mStart: mEnd]
    std = np.std(sample)
    if std > stdThreshold: continue
    model = LinearRegression()
    X,y = np.array(range(sample.shape[0])).reshape(-1,1), sample
    model.fit(X,y)
    coef = model.coef_[0]
    if coef > slopeThreshold: continue
    meanValue = np.mean(sample)
    target.append({"range":(start, end), 'mean': meanValue})
    # print((start, end), std, coef)

newTarget = {}

for elem in target:
    meanStr = str(elem['mean'])
    mRange = elem['range']
    newTarget.update({})

for elem in newTarget:

import matplotlib.pyplot as plt

# plt.plot(xLeftPoints)
# plt.plot(xLeftPointsFiltered)
# plt.plot(xLeftPointsFilteredDiff)
# # plt.plot(xLeftPointsFilteredDiff3)
# plt.plot(xLeftPointsSignalFiltered)
# plt.show()


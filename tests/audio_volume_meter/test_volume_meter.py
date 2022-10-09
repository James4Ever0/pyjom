# usually yelling is not always funny. but we can do speech to text. taking longer time though... pinpoint the cue time.

# often some exclamation attempts like repetation or louder sounds.

audio_src = "/media/root/help/pyjom/samples/audio/dog_with_text/vocals.wav"

# heard of dog woooling.
# import audioop

import pydub

timestep = 0.1  # my time setting.
audiofile = pydub.AudioSegment.from_wav(audio_src)
frame_rate = audiofile.frame_rate
seconds = audiofile.duration_seconds
print(frame_rate)  # 44100.
print(seconds)  # sample length

import math
import numpy as np
from talib import stream

# frame_rate2 = frame_rate *timestep
milistep = 1000 * timestep
ma_step = 10  # one second of buffer size. or more. timeperiod=ma_step

std_arr, maxval_arr, abs_nonzero_arr = [], [], []


def getPaddingMovingAverage(myarray, timeperiod=10):
    lt = math.ceil(timeperiod / 2)
    rt = timeperiod - lt
    len_myarray = len(myarray)
    max_index = len_myarray - 1
    result_array = []
    for i in range(len_myarray):
        start_index = i - lt
        start_index = max(0, start_index)
        end_index = i + rt
        end_index = min(end_index, max_index)
        array_slice = myarray[start_index:end_index]
        arr_slice_length = end_index - start_index
        val = sum(array_slice) / arr_slice_length
        # val = np.median(array_slice)
        result_array.append(val)
    return result_array


msteps = math.ceil(seconds / timestep)

for i in range(msteps):
    # print(frame_rate2)
    # probably in miliseconds.
    segment = audiofile[i * milistep : (i + 1) * milistep]
    data = segment.get_array_of_samples()
    # containes two channels. 4410*2
    darray = np.array(data)
    print(darray.shape)
    std = np.std(darray)
    abs_darray = abs(darray)
    maxval = np.max(abs_darray)
    abs_nonzero = np.average(abs_darray)
    print("STD:{} MAX:{} AVG:{}".format(std, maxval, abs_nonzero))
    std_arr.append(std)
    # ma_std = stream.SMA(np.array(std_arr[-ma_step:]).astype(np.float64))
    maxval_arr.append(maxval)
    # ma_maxval = stream.SMA(np.array(maxval_arr[-ma_step:]).astype(np.float64))
    abs_nonzero_arr.append(abs_nonzero)
    # ma_abs_nonzero = stream.SMA(np.array(abs_nonzero_arr[-ma_step:]).astype(np.float64))
    # breakpoint()
    # print("MA_STD:{} MA_MAX:{} MA_AVG:{}".format(ma_std,ma_maxval,ma_abs_nonzero))
    # print(data)
    # breakpoint()
    # maxAudioValue =audioop.max(data,2)
    # print("STEP:",i,"VOLUME:",maxAudioValue)
std_arr0 = getPaddingMovingAverage(std_arr, timeperiod=20)
maxval_arr0 = getPaddingMovingAverage(maxval_arr, timeperiod=20)
abs_nonzero_arr0 = getPaddingMovingAverage(abs_nonzero_arr, timeperiod=20)

ma_std_arr = getPaddingMovingAverage(std_arr, timeperiod=60)
ma_maxval_arr = getPaddingMovingAverage(maxval_arr, timeperiod=60)
ma_abs_nonzero_arr = getPaddingMovingAverage(abs_nonzero_arr, timeperiod=60)
# just use one freaking example as my conclusion.
status = "end"
vocal_slices = []
vocal_slice = []
final_index = msteps - 1
# could you use clustering.
# like time versus duration.
avg_std = []
for i in range(msteps):
    a, b, c = std_arr0[i], maxval_arr0[i], abs_nonzero_arr0[i]
    a0, b0, c0 = ma_std_arr[i], ma_maxval_arr[i], ma_abs_nonzero_arr[i]
    if status == "end":
        # startpoint = a0 < a
        startpoint = a0 < a or b0 < b or c0 < c
        if startpoint:
            vocal_slice.append(i)
            avg_std.append(a)
            status = "start"
    else:
        avg_std.append(a)
        # endpoint = a0 > a
        endpoint = a0 > a and b0 > b and c0 > c
        if endpoint:
            vocal_slice.append(i)
            # vocal_slice[1] = i
            status = "end"
            vocal_slices.append([vocal_slice, np.average(avg_std)])
            vocal_slice = []
            avg_std = []
if len(vocal_slice) == 1:
    vocal_slice.append(final_index)
    vocal_slices.append([vocal_slice, np.average(avg_std)])

time_rate = timestep
timed_vocal_slices = [
    [[x[0][0] * time_rate, x[0][1] * time_rate], x[1]] for x in vocal_slices
]
d2_data = []
d1_data = []
for slice_vocal in timed_vocal_slices:
    print(slice_vocal)  # it could be two dimentional. both for length and volume?
    # to find best shit you need grouping.
    a, b = slice_vocal[0]
    length = b - a
    d2_data.append([length, slice_vocal[1]])
    d1_data.append([slice_vocal[1]])

from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=2)
km = kmeans.fit(d1_data)
labels = km.labels_
label_indexs = {i: labels[i] for i in range(len(labels))}
# print(label_index)
new_labels = []
mergeTimeGap = 0.5
lb_new = 0
last_elem = None
for index, data in enumerate(timed_vocal_slices):
    # data = timed_vocal_slices
    [start, end], std = data
    label = label_indexs[index]
    if last_elem == None:
        last_elem = [[start, end], label]
    else:
        [[last_start, last_end], last_label] = last_elem
        if start - last_end < mergeTimeGap and last_label == label:
            pass
            # last_elem = [[start,end],label]
        else:
            lb_new += 1
        last_elem = [[start, end], label]

    new_labels.append(lb_new)
    print("DATA:", data, "LABEL:", label, "NEW_LABEL:", lb_new)

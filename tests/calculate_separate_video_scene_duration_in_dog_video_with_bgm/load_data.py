import pandas

metric = "video.stats.csv"
metric = pandas.read_csv(metric)

scenes = "sample_scenes.csv"

with open(scenes, "r") as f:
    content = f.read()
    lines = content.split("\n")
    timecodeList = lines[0]
    scenes = "\n".join(lines[1:])
    from io import StringIO

    scenes = StringIO(scenes)

timecodeList = timecodeList.split(",")
timecodeList[0] = "00:00:00.000"

scenes = pandas.read_csv(scenes)

lengths = []
sceneCuts = []
for index, row in scenes.iterrows():
    # print(row)
    # breakpoint()
    start, end = row["Start Timecode"], row["End Timecode"]
    length = row["Length (seconds)"]

    sceneCuts.append((start, end, length))
    # print(start, end)
    # please calculate the length!
    lengths.append(length)
    # print(length, type(length)) # float.

flag = "filter"
filename = "sample.mp4"

if flag == "calculate_statistics":
    import numpy

    std = numpy.std(lengths)
    mean = numpy.mean(lengths)
    print(std, mean)
    # 1.6674874515595588 2.839698412698412
    print(min(lengths), max(lengths))
    min(lengths), max(lengths)
    # 0.6 7.833
    # strange though.
    # shall we adjust this accordingly? how to generate this shit?
elif flag == "generate_ffplay":
    for (start, end, duration) in sceneCuts:
        print("ffplay -ss %s -t %s -i %s -autoexit " % (start, duration, filename))
        print("sleep 3")
elif flag == "render":
    import os
    import datetime

    durationThreshold = 0.6674874515595588
    mTimeDelta = datetime.timedelta(milliseconds=100)  # 0.1 seconds
    getTimeObject = lambda timeString: datetime.datetime.strptime(
        timeString, "%H:%M:%S.%f"
    )
    getTimeString = lambda timeObject: timeObject.strftime("%H:%M:%S.%f")
    if not os.path.exists("output"):
        os.mkdir("output")
    for index, (start, end, duration) in enumerate(sceneCuts):
        estimatedDuration = duration - 0.2
        if estimatedDuration < durationThreshold:
            continue
        start2 = getTimeObject(start) + mTimeDelta
        end2 = getTimeObject(end) - mTimeDelta
        start2, end2 = getTimeString(start2), getTimeString(end2)
        output = "output/%d.flv" % index
        print("ffmpeg -y -ss %s -to %s -i %s  %s" % (start2, end2, filename, output))
elif flag == "filter": # to make sure the selected set will be evenly spaced. no two elements will get closer to each other than 5 seconds.
    import random
    fakeQualificationFunction = lambda: random.randrange(0.6674874515595588,7.833)
    candidates = []
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

flag = "render"
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
    for( start, end, duration) in sceneCuts:
        print("ffplay -ss %s -t %s -i %s -autoexit " % (start, duration, filename))
        print("sleep 3")
elif flag == "render":
    import os
    import datetime
    getTimeObject = lambda timeString: datetime.datetime.strptime(timeString,"%H:%M:%S.%f")
    getTimeString = lambda timeObject: timeObject.strftime("%H:%M:%S.%f")
    if not os.path.exists("output"):
        os.mkdir("output")
    for index,( start, end, duration) in enumerate(sceneCuts):
        output = "output/%d.flv" % index
        print("ffmpeg -y -ss %s -to %s -i %s  %s" % (start, end, filename, output))
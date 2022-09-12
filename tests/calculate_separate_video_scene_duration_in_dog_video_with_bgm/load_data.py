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
    sceneCuts.append((start, end))
    # print(start, end)
    # please calculate the length!
    length = row['Length (seconds)']
    lengths.append(length)
    # print(length, type(length)) # float.

flag = "generate_ffplay"
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
    filename = "sample.mp4"
    for start, end in sceneCuts:
        print("ffplay -i %s -ss %s -to %s" %( filename, start, end))
        print('sleep 3')
import pandas

metric = 'video.stats.csv'
metric = pandas.read_csv(metric)

scenes = 'sample_scenes.csv'
 
with open(scenes, 'r') as f:
    content = f.read()
    lines = content.split("\n")
    timecodeList = lines[0]
    scenes = "\n".join(lines[1:])
    from io import StringIO
    scenes = StringIO(scenes)

timecodeList =timecodeList.split(",")
timecodeList[0] = "00:00:00.000"

scenes = pandas.read_csv(scenes)

for row in scenes.iterrows():
    start, end = row['Start Timecode'],row['End Timecode']
    print(start, end)
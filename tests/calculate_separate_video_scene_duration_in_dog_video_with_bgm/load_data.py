import pandas

metric = 'video.stats.csv'
metric = pandas.read_csv(metric)

scenes = 'sample_scenes.csv'
 
with open(scenes, 'r') as f:
    content = f.read()
    lines = content.split("\n")
    timecodeList = lines[0]
    scenes = "\n".join(lines[1:])
    scenes = from io import StringIO

scenes = pandas.read_csv(scenes)

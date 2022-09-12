import pandas

metric = 'video.stats.csv'
metric = pandas.read_csv(metric)

scenes = 'sample_scenes.csv'
 
with open(scenes, 'r') as f:
    content = f.read()

scenes = pandas.read_csv(scenes)

import pandas

metric = 'video.stats.csv'
metric = pandas.read_csv(metric)

scenes = 'sample_scenes.csv'
 
with open(scenes, 'r') as f:
    content = f.read()
    lines = content.split("\n")
    

scenes = pandas.read_csv(scenes)

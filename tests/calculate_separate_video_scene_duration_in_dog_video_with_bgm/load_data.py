import pandas

metric = 'video.stats.csv'
metric = open(metric,'r').read()
metric = pandas.load_csv(metric)
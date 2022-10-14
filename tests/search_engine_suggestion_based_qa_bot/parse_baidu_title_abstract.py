from lazero.filesystem.io import readJsonObjectFromFile

data = readJsonObjectFromFile('result_baidu.json')

for elem in data:
    title = elem.get('title')
    abstract = elem.get('abstract')
    
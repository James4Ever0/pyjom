import requests
import time
import json

def getJson(pageIndex=1, pageSize=16):
    url = 'https://api.hubble.jina.ai/v2/rpc/executor.list'
    query = {"sort":"-activities.metaMatched","pageIndex":pageIndex,"pageSize":pageSize,"search":"","author":"","keywords":[],"withAnonymous":True}
    r = requests.post(url,json=query)
    jsonData = r.json()
    return jsonData

pageSize = 16
jsonData = getJson(pageSize=pageSize)
total = jsonData["meta"]["total"]
print('total:', total)
data = [jsonData.copy()]


import math
pages = math.ceil(total/pageSize)
import progressbar
for index in progressbar.progressbar(range(2,pages+1)):
    time.sleep(2)
    # print('page index:',index)
    jsonData = getJson(pageIndex=index, pageSize=pageSize)
    data.append(jsonData.copy())

print("writing data")
with open("")
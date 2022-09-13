import requests
import time
def getJson(pageIndex=1, pageSize=16):
    url = 'https://api.hubble.jina.ai/v2/rpc/executor.list'
    query = {"sort":"-activities.metaMatched","pageIndex":pageIndex,"pageSize":16,"search":"","author":"","keywords":[],"withAnonymous":True}
    r = requests.post(url,json=query)
    jsonData = r.json()
total = jsonData["meta"]["total"]
print('total:', total)
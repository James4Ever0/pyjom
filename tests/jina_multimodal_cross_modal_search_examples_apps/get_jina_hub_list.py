import requests

url = 'https://api.hubble.jina.ai/v2/rpc/executor.list'
requests.get({"sort":"-activities.metaMatched","pageIndex":3,"pageSize":16,"search":"","author":"","keywords":[],"withAnonymous":true}' \
  --compressed
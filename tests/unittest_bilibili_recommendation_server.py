import requests

baseurl = "http://localhost:"

r = requests.get(baseurl)
print(r.text)
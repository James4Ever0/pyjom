import requests
port=
baseurl = "http://localhost:{}".format(port)

r = requests.get(baseurl)
print(r.text)
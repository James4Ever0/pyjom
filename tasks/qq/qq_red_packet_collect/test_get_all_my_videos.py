import requests
port, endpoint = 7341,"searchUserVideos"
postData = {}
r = requests.post(f"http://localhost:{port}/{endpoint}", data=postData)
data = r.json()
print("data")
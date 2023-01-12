import requests
port, endpoint = 7341,"searchUserVideos"
params = {}
r = requests.get(f"http://localhost:{port}/{endpoint}", params=params)
data = r.json()
print("data")
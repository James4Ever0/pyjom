import requests
port, endpoint = 7341,"searchUserVideos"
postData = {'query':'abc','method':'online'}
r = requests.post(f"http://localhost:{port}/{endpoint}", json=postData)
data = r.json()
print("data")
import requests

port, endpoint = 7341, "searchUserVideos"

postData = {"query": "猫", "tid": 0, "method": "bm25"}
r = requests.post(f"http://localhost:{port}/{endpoint}", json=postData)
data = r.json()
print("data")

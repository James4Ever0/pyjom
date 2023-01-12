import requests

port, endpoint = 7341, "searchUserVideos"

postData = {"query":"", "tid": 0, "method": "online"} # this is to get latest video of my own. fuck. better turned into registration based method.
r = requests.post(f"http://localhost:{port}/{endpoint}", json=postData)
data = r.json()
print("data")
import rich
rich.print(data)

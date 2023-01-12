import requests
port, endpoint = ,""
params = {}
r = requests.get(f"http://localhost:{port}/{endpoint}", params=params)
data = r.json()
print("data")
import json


with open("search_result_all.json", "r") as f:
    data = f.read()
    data = json.loads(data)

import json

test_subject == "search_all"

if test_subject == "search_all":
    with open("search_result_all.json", "r") as f:
        data = f.read()
        data = json.loads(data)
    results = data['result']
    for elem in results:
        try:
            if elem['result_type'] == 'video':
                for video in elem['data']:
                    if video['type']
        except:
            pass
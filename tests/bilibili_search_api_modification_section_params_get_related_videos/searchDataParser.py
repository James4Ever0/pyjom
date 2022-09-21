import json
from bs4 import BeautifulSoup

def clearHtmlTags(htmlObject):
    a = BeautifulSoup(htmlObject, features='lxml')
    return a.text

test_subject = "search_all"

if test_subject == "search_all":
    with open("search_result_all.json", "r") as f:
        data = f.read()
        data = json.loads(data)
    results = data['result']
    for elem in results:
        try:
            if elem['result_type'] == 'video':
                for video in elem['data']:
                    try:
                        if video['type'] == 'video':
                            bvid = video['bvid'] 
                            tag = video['tag']
                            tags = tag.split(",")
                            title = video['title'] # remove those markers, please?
                            title = clearHtmlTags(title)
                            duration = video['duration']
                            play = video['play'] # select some hot videos.
        except:
            pass
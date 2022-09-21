import json
from bs4 import BeautifulSoup
from lazero.utils.logger import sprint

def linkFixer(link,prefix="https:"):
    if link.startswith("//"):
        return prefix+link
    return link

def traceError(errorMsg:str="error!", _breakpoint:bool=False):
    import traceback
    traceback.print_exc()
    sprint(errorMsg)
    if _breakpoint:
        return breakpoint()

def videoDurationStringToSeconds(durationString):
    durationString = durationString.strip()
    mList = durationString.split(":")[::-1]
    if len(mList) > 3:
        print("DURATION STRING TOO LONG")
        return None
    seconds = 0
    for index, elem in enumerate(mList):
        elem = int(elem)
        seconds += (60**index)*elem
    return seconds

def clearHtmlTags(htmlObject):
    a = BeautifulSoup(htmlObject, features='lxml')
    return a.text



def parseSearchResult(data):
    results = data['result']
    for elem in results:
        try:
            if elem['result_type'] == 'video':
                for video in elem['data']:
                    # be warned cause all these things might fail.

        except:
            traceError('error iterating data results')

test_subject = "search_video"
# test_subject = "search_all"

if test_subject == "search_all":
    with open("search_result_all.json", "r") as f:
        data = f.read()
        data = json.loads(data)
    parseSearchResult(data)
elif test_subject == "search_video":
    with open("search_by_type_result_video.json", "r") as f:
        data = f.read()
        data = json.loads(data)
    parseSearchResult(data)
else:
    raise Exception("unknown test_subject:", test_subject)
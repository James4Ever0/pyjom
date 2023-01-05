
import rich

catSignals = ["喵喵", "猫", "猫咪", "喵"]

dogSignals = [
    "狗狗",
    "狗",
    "汪汪",
    "修勾",
    "汪",
    "狗子",
]

# def getQueryWordFromSignals(signals:list):
#     msignals = signals.copy()
#     msignals.sort(key=lambda x: len(x))
#     response = []
#     for s in msignals:
#         if s not in " ".join(response):
#             response.append(s)
#     return " ".join(response)

catDogElemDict = {"cat": catSignals, "dog": dogSignals}
# catQueryWord = getQueryWordFromSignals(catSignals)
# dogQueryWord = getQueryWordFromSignals(dogSignals)
# # print("DOG QUERY WORD?",dogQueryWord)
# catDogQueryWords = {"cat": catQueryWord,"dog":dogQueryWord}

def checkCatOrDog(Content: str):
    # cat? dog? None?

    for key, elems in catDogElemDict.items():
        for elem in elems:
            if elem in Content.lower():
                return key
    return None

# pip3 install python_cypher
# pip3 install neo4j
from functools import lru_cache

@lru_cache(maxsize=1)
def getNeo4jDriver(address="neo4j://localhost:7687",username="neo4j", password="kali",debug=False): # so we bruteforced it. thanks to chatgpt.
    from neo4j import GraphDatabase
    driver = GraphDatabase.driver(address,
                                auth=(username,password))
    if debug:
        print("login successful: username:%s password:%s" % (username, password))
    return driver

from pypher import Pypher

def makeCatOrDogConnections(group_id:str, sender_id:str, cat_or_dog:str, debug:bool=False, delete:bool=False): # whatever.
    # Create a new Pypher object
    with getNeo4jDriver().session() as session:
        p = Pypher()
        if delete:
            p.MATCH.node('n1',labels='qq_group', group_id=group_id)
            p.MATCH.node('n2',labels ='qq_user', user_id=sender_id)
            p.MATCH.node('n3',labels ='ad_keyword', keyword=cat_or_dog) # fine.
            p.DETACHDELETE.node('n1').DETACHDELETE.node('n2').DETACHDELETE.node('n3')

        # Use the MERGE clause to create the nodes if they do not already exist
        else:
            p.MERGE.node('n1',labels='qq_group', group_id=group_id)
            p.MERGE.node('n2',labels ='qq_user', user_id=sender_id)
            p.MERGE.node('n3',labels ='ad_keyword', keyword=cat_or_dog)

            # Use the MERGE clause to create the relationship between the nodes if it does not already exist
            p.MERGE.node('n1').rel_out('r', labels='includes').node('n2')
            p.MERGE.node('n2').rel_out('r1', labels='talks_of').node('n3')

        # Generate the Cypher query string
        query = str(p)
        if debug:
            print("QUERY?", query)
            print("QUERY TYPE?", type(query))
            # how to roll back?
        # Execute the query using the Neo4j driver
        result = session.run(query, parameters=p.bound_params)
        if debug:
            print("RESULT?", result)

from lazero.network.checker import waitForServerUp

BILIBILI_RECOMMENDATION_SERVER_PORT = 7341

waitForServerUp(BILIBILI_RECOMMENDATION_SERVER_PORT,"bilibili recommendation server")

import requests
# import random
from bilibili_api.search import bilibiliSearchParams

# you might just want some delay when searching online.

def getCatOrDogAd(cat_or_dog:str,server:str = "http://localhost:{}".format(BILIBILI_RECOMMENDATION_SERVER_PORT),debug:bool=False):
    # how do we get one? by label? by category? by name?
    url = server+"/searchUserVideos"

    # queryWord = catDogQueryWords.get(cat_or_dog,None)
    queryWords = catDogElemDict.get(cat_or_dog,None)
    try:
        assert queryWords is not None
    except Exception as e:
        print("Could not find topic with keyword:",cat_or_dog)
        raise e
    
    animalTid = bilibiliSearchParams.video.tids.动物圈.tid
    # myTids = {"cat":bilibiliSearchParams.video.tids.动物圈.喵星人,"dog":bilibiliSearchParams.video.tids.动物圈.汪星人}
    # myTid = myTids[cat_or_dog]
    # queryWord = random.choice(["",random.choice(queryWords)]) # you can still have things without query
    # queryWord = " ".join(queryWords)
    # queryWord = {"cat":'猫',"dog":'狗'}[cat_or_dog] # Whatever. fuck it. replace it with semantic search later? or you use multiple searches.

    # you cannot just ignore the queryWord in bm25
    responses = []
    for queryWord in queryWords:
        # data = {"query":queryWord,"tid":random.choice([0]*20+[animalTid]*10+[myTid]*5)} # you can specify my user id. you may make that empty?
        data = {"query":queryWord,"tid":animalTid,'method':'bm25'}
        if debug:
            print("POSTING DATA:")
            rich.print(data)

        r = requests.post(url,json=data)
        response = r.json()
        for elem in response:
            if elem not in responses:
                responses.append(elem)
    responses.sort(key=lambda elem:-elem.get('pubdate',-1))
    if debug:
        print("RESPONSES?")
        rich.print(responses)
    return responses # select one such response.

def generateAdFromVideoInfo(videoInfo):
    # selected video info.
    bvid, pic, title = videoInfo['bvid'], videoInfo['pic'], videoInfo['title']

from botoy import Action
def sendCatOrDogAd(group_id:str, cat_or_dog:str,action:Action):
    sendMessageStatus = action.sendGroupText(
                        group=group_id, content=reply
    )
                    # stderrPrint("SENT MESSAGE STATUS:",sendMessageStatus)
    success = (
        sendMessageStatus["ErrMsg"] == ""
        and sendMessageStatus["Ret"] == 0
    )
    return success
def checkCatOrDog(Content: str):
    # cat? dog? None?
    catSignals = ["喵喵", "猫", "猫咪", "喵"]

    dogSignals = [
        "狗狗",
        "狗",
        "汪汪",
        "修勾",
        "汪",
        "狗子",
    ]
    dogSignals = []
    elemDict = {"cat": catSignals, "dog": dogSignals}
    for key, elems in elemDict.items():
        for elem in elems:
            if elem in Content.lower():
                return key
    return None

# pip3 install python_cypher
# pip3 install neo4j
from functools import lru_cache

def getNeo4jDriver(address="neo4j://localhost:7687",username="neo4j", password="password" ):
    from neo4j import GraphDatabase
    driver = GraphDatabase.driver(address,
                                auth=(username,password))
    return driver

from pypher import Pypher
def makeCatOrDogConnections(group_id:str, sender_id:str, cat_or_dog:str): # whatever.

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

@lru_cache(maxsize=1)
def getNeo4jDriver(address="neo4j://localhost:7687",username="neo4j", password="kali",debug=False): # so we bruteforced it. thanks to chatgpt.
    from neo4j import GraphDatabase
    driver = GraphDatabase.driver(address,
                                auth=(username,password))
    if debug:
        print("login successful: username:%s password:%s" % (username, password))
    return driver

from pypher import Pypher
def makeCatOrDogConnections(group_id:str, sender_id:str, cat_or_dog:str, debug:bool=False): # whatever.
    # Create a new Pypher object
    with getNeo4jDriver().session() as session:
        p = Pypher()

        # Use the MERGE clause to create the nodes if they do not already exist
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

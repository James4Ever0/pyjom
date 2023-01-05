
from adtools import getNeo4jDriver

def test_login():
    usernames = ['kali','user','neo4j','admin', 'parrot']
    passwords = ['neo4j', 'kali','parrot', 'admin', 'password']
    for u in usernames:
        for p in passwords:
            try:
                getNeo4jDriver(username=u, password=p,debug=False)
            except:
                pass

from adtools import getNeo4jDriver

def test_login():
    usernames = ['kali','user','neo4j','admin', 'parrot']
    passwords = ['neo4j', 'kali','parrot', 'admin', 'password']
    for u in usernames:
        for p in passwords:
            try:
                print("USING:",u,p)
                r = getNeo4jDriver(username=u, password=p,debug=False)
                # print('RESPONSE?',r)
                with driver.session() as session:
    result = session.run("MATCH (n) RETURN n LIMIT 1")
    print(result.single())

            except:
                import traceback
                traceback.print_exc()
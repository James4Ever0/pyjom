from adtools import getNeo4jDriver


def test_login():
    usernames = ["kali", "user", "neo4j", "admin", "parrot", ""]
    passwords = ["neo4j", "kali", "parrot", "admin", "password", ""]
    for u in usernames:
        for p in passwords:
            try:
                driver = getNeo4jDriver(username=u, password=p, debug=False)
                # print('RESPONSE?',r)
                with driver.session() as session:
                    result = session.run("MATCH (n) RETURN n LIMIT 1")
                    print(result.single())
                    print("USING:", u, p)
            except:
                pass
                # import traceback
                # traceback.print_exc()

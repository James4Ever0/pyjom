def troubleFunction():
    statementsAtSameLevel = [
        "f = 12",
        "return a",
        "return b",
        "return c",
        "return d",
        "return e",
        "return f",
    ]
    for statement in statementsAtSameLevel:
        print("executing statement:", statement)
        while True:
            try:
                if statement.startswith("return "):
                    print("eval return statement")
                    val = eval(statement.replace("return ", ""))
                    return val
                else:
                    print("exec normal statement")
                    exec(statement)
                break
            except:
                import traceback

                traceback.print_exc()
                print("error code:", statement)
                statement = input("please enter remedy:\n")


val = troubleFunction()
print("get value:", val)

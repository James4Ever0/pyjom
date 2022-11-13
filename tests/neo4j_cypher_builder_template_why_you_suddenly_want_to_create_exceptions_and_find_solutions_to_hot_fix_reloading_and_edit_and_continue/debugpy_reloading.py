
def program():
    raise Exception("Exception in program")
    return "VALUE"

while True:
    try:
        val = program()
        print("returned value:", val)
    except:
        input('are you finished?')
        import importlib
        # importlib.reload(program)
        print(importlib.__cached__)
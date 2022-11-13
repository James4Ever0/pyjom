
def program():
    raise Exception("Exception in program")
    return "VALUE"

while True:
try:
    val = program()
    print("returned value:", val)
except:
    import importlib
    importlib.reload(".")
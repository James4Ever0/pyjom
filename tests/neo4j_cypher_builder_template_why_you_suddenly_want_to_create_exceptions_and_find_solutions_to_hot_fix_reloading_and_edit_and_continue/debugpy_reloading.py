
# use bpython?
def program():
    raise Exception("Exception in program")
    return "VALUE"

try:
    val = program()
    print("returned value:", val)
except:
    import importlib
    importlib.reload(".")
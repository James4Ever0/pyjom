
# use bpython?
def ():
    raise Exception("oh shit")
    return "VALUE"

try:
    val = shit()
    print("returned value:", val)
except:
    import importlib
    importlib.reload(".")
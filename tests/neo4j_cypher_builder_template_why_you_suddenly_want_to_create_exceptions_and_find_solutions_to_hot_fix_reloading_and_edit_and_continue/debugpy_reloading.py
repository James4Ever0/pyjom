# let's raise shit.

# use bpython?
def shit():
    raise Exception("oh shit")
    return "VALUE"

try:
    val = shit()
    print("returned value:", val)
except:
    import importlib
    importlib.reload()

def program():
    raise Exception("Exception in program")
    return "VALUE"

while True:
    try:
        from my_module import program
        val = program()
        print("returned value:", val)
    except:
        import traceback
        traceback.print_exc()
        import importlib
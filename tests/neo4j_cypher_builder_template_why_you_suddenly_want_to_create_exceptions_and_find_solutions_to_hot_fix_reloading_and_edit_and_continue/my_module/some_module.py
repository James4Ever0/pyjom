# inside some_module.py

def program():
    raise Exception("Exception in program")
    # return "VALUE"

if __name__ == "__main__":
    while True:
        try:
            import some_module # will it even succeed? doubt this.
            val = some_module.program()
            print("returned value:", val)
            break
        except:
            import traceback
            traceback.print_exc()
            input('are you done yet?')
            import importlib
            importlib.reload(some_module)

def program():
    # raise Exception("Exception in program")
    return "VALUE"

if __name__ == "__main__":
    while True:
        try:
            import some_module
            val = some_module.program()
            print("returned value:", val)
        except:
            import traceback
            traceback.print_exc()
            input('are you done yet?')
            import importlib
            importlib.reload(some_module)
            break
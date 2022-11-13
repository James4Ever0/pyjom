
def program():
    raise Exception("Exception in program")
    return "VALUE"

if __name__ == "__main__":
    while True:
        try:
            from some_module import program
            val = program()
            print("returned value:", val)
        except:
            import traceback
            traceback.print_exc()
            import importlib
            importlib.reload(my_module)
def error_func():
    try:
        return a
    except:
        print('you must somehow return something')
        breakpoint() # use pdb?

error_func()
def error_func():
    try:
        return a
    except:
        print('you must somehow return something')
        breakpoint() # use pdb?

val = error_func()
print('value returned:',val)
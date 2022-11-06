def error_func():
    try:
        return a
    except:
        print('you must somehow return something')
        exec(
        input('please set some return statement.')
        return val

val = error_func()
print('value returned:',val)
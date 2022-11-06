def error_func():
    try:
        return a
    except:
        print('you must somehow return something')
        while True:
            code = input('please set some return statement.')
            if code.startswith('return '):
                exec("myReturnValue = {}".format(code.replace('return ','')))
                return myReturnValue

val = error_func()
print('value returned:',val)
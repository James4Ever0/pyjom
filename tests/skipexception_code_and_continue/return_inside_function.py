def error_func():
    try:
        return a
    except:
        print('you must somehow return something')
        while True:
            code = input('please set some return statement.')
            if code.startswith('return '):
                myReturnValue = exec("{}".format(code.replace('return ','')))
                return myReturnValue
            else:
                exec(code)

val = error_func()
print('value returned:',val)
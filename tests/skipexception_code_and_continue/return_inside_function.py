
def error_func():
    try:
        return a
    except:
        print('you must somehow return something')
        while True:
            code = input('please set some return statement.\n')
            if code.startswith('return '):
                myReturnValue = eval("{}".format(code.replace('return ','')))
                print('about to return value')
                return myReturnValue
            else:
                exec(code)

val = error_func()
print('value returned:',val)
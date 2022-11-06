def troubleFunction():
    statementsAtSameLevel = ['f = 12','return a','return b','return c','return d','return e','return f']
    for statement in statementsAtSameLevel:
        while True:
            try:
                if statement.startswith('return '):
                    val = eval(statement.replace('return ',''))
                    return val
                else:
                    exec(statement)
            except:
                print('error code: %d' % statement)
                statement = input('please enter remedy:\n')
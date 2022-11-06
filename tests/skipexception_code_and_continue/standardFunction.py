def troubleFunction():
    statementsAtSameLevel = ['f = 12','return a','return b','return c','return d','return e','return f']
    for statement in statementsAtSameLevel:
        if statement.startswith('return '):
            val = eval(statement.replace('return ',''))
            return val
        else:
            exec()
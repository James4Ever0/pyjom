def generator():
    for index in range(100):
        yield index

def generator2():
    yield from generator() # this is to simplifying the process of iteration.

def iterator(lambdaFunction):
    for _ in range(4):
        result = lambdaFunction()
        print(result)

def generator3():
    myGenerator = generator2()
    getNextNumber = lambda: myGenerator.__next__()
    for _ in range(3):
    iterator(getNextNumber)

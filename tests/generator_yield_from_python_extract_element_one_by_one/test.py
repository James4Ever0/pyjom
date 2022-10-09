def generator():
    for index in range(100):
        yield index

def generator2():
    yield from generator() # this is to simplifying the process of iteration.



myGenerator = generator2()
getNextNumber = lambda: myGenerator.__next__()
for _ in range(20):
    result = getNextNumber()  # good.
    print("iterate result:", result)

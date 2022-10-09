def generator():
    for index in range(100):
        yield index

myGenerator = generator()
for _ in range(20):
    result = myGenerator.__iter__().
    print('iterate result:', result)
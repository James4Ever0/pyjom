def generator():
    for index in range(100):
        yield index

for _ in range(20):
    yield from myGenerator
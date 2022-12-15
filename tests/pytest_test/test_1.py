def non_test():
    print("no test")
    return 1

class ValueStorage:
    value1 = None
    value2 = None

def test_a():
    ValueStorage.value1 = 1
    print("TEST!")

def test_b():
    print("test b") # no printing?
    assert ValueStorage.value1 == 1
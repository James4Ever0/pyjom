def non_test():
    print("no test")
    return 1

class ValueStorage:
    value1 = None
    value2 = None

def test_a():
    ValueStorage.value1 = 1
    from non_test import shit
    shit()
    print("TEST!") # does have traceback.

def test_b():
    print("test b") # no printing?
    assert ValueStorage.value1 == 1

def test_c():
    assert ValueStorage.value2 == 1
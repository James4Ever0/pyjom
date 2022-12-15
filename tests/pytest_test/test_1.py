def non_test():
    print("no test")
    return 1

def test_a():
    print("TEST!")

def test_b():
    test_a()
    print("test b") # no printing?
    assert 1 == 1
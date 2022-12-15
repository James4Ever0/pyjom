def non_test():
    print("no test")
    return 1

class test_class():
    # use class?
    def test_a(self):
        self.a = 1
        print("TEST!")

    def test_b(self):
        print("test b") # no printing?
        assert self.a == 1
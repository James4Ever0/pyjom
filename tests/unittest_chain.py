# how to chain functions?

class add(bool):
    def __call__(self, *args):
        return add(self + n)
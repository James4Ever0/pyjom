# how to chain functions?

class add(bool):
    def __call__(self, n):
        return add(self + n)
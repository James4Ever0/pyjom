# how to chain functions?

class add(bool):
    def __call__(self, n):
        if self == True:
        return add(self + n)
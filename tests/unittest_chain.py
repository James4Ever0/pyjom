# how to chain functions?

class myBool(bool):
    def __call__(self, n):
        if self == False: return False
        return myBool(n)
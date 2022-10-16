# a dynamic property in set


class Obj:
    def __init__(self):
        self.val = 0

    @property
    def prop(self):
        self.val += 1
        return self.val


obj = Obj()
# mproperty = obj.prop
myData = [{"a": lambda: obj.prop}] * 2

for d in myData:
    val = d["a"]()
    print(val)
# for _ in range(3):
#     print(obj.prop) # strange.

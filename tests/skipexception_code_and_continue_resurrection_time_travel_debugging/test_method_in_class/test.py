from reloading import reloading

class a:
    @reloading # does this work?
    def someMethod(self):
        # raise Exception('shit')
        

A = a()
A.someMethod()
from reloading import reloading

class a:
    @reloading # does this work?
    def someMethod(self):
        # raise Exception('shit')
        raise Exception('another shit')

A = a()
A.someMethod()
from reloading import reloading

class a:
    @reloading
    def someMethod(self):
        raise Exception('shit')
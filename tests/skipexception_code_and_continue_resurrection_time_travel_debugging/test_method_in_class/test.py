from reloading import reloading
import asyncio

def mreload(mclass):
    class newclass:
        def __init__(self, *args, **kwargs):
            print('good')
    return newclass

class Mydecorator:
    #accept the class as argument
    def __init__(self, student):
        print("STUDENT:", student)
        self.class_ = student
    
    #accept the class's __init__ method arguments
    def __call__(self,*args, **kwargs):
        #define a new display method
        print('CALL ARGS', args)
        print('CALL KWARGS',kwargs)
        class_ = self.class_()

# @mreload
@Mydecorator
class a:
    # raise Exception('shit')
    # cannot raise exception here. the compiler will complain.
    # good?
    @reloading # does this work?
    def someMethod(self):
        # @reloading # this will not work.
        def someothermethod():
            # raise Exception('just another shit')
            return 'value'
        # raise Exception('just another shit')
        val = someothermethod()
        return val
    @reloading
    async def someOtherMethod(self): # cannot decorate async function?
        # raise Exception('just another shit')
        return 'good'
    @reloading
    def runAsync(self):
        loop= asyncio.get_event_loop()
        val = loop.run_until_complete(self.someOtherMethod())
        print('value from async func:', val)
        return val


A = a('abcdef')
print(A)
breakpoint()
# val = A.someMethod()
val = A.runAsync()
print('return value:', val)
# print('shit')
# print('good')
from reloading import reloading
import asyncio
class a:
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
    async def someOtherMethod(self):
        raise Exception('shit')
    
    @reloading
    def runAsync(self):


A = a()
val = A.someMethod()
print('return value:', val)
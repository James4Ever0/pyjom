from reloading import reloading
import asyncio

@reloading
class a:
    raise Exception('shit')
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


A = a()
# val = A.someMethod()
val = A.runAsync()
print('return value:', val)
from reloading import reloading
import asyncio

@reloading
class a:
    someval = 1
    @reloading
    def someMethod(self):
        @reloading
        def someothermethod():
            # raise Exception('but just another shit')
            return 'value'
        # raise Exception('just another shit')
        val = someothermethod()
        return val
    @reloading
    async def someOtherMethod(self): # cannot decorate async function?
        # raise Exception('just another shit')
        @reloading
        async def shit():
            # raise Exception('but just and but just another shit')
            return 'abcdef'
        val = await shit()
        return val
    @reloading
    def runAsync(self):
        loop= asyncio.get_event_loop()
        val = loop.run_until_complete(self.someOtherMethod())
        print('value from async func:', val)
        return val

@reloading
def main():
    A = a() # shit
    print(A)
    # breakpoint()
    # val = A.someMethod()
    val = A.runAsync()
    print('return value:', val)
    # print('shit')
    print('good')

main()
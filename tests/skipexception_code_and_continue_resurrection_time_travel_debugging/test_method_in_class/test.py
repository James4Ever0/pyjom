from reloading import reloading
import asyncio

@reloading
class a:
    someval = 1
    @reloading
    def someMethod(self):
        @reloading
        def someothermethod():
            raise Exception('exception1')
            return 'value'
        raise Exception('exception2')
        val = someothermethod()
        return val
    @reloading
    async def someOtherMethod(self):
        # raise Exception('async exception1')
        @reloading
        async def shit():
            # raise Exception('async exception2')
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
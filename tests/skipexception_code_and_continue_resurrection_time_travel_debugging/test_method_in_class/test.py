from reloading import reloading
import asyncio

@reloading
class myClass:
    someval = 1
    @reloading
    def someMethod(self):
        @reloading
        def someInnerMethod():
            raise Exception('exception1')
            return 'value'
        raise Exception('exception2')
        val = someInnerMethod()
        return val
    @reloading
    async def someOtherMethod(self):
        # raise Exception('async exception1')
        @reloading
        async def asyncInside():
            raise Exception('async exception2')
            return 'abcdef'
        val = await asyncInside()
        return val
    @reloading
    def runAsync(self):
        loop= asyncio.get_event_loop()
        val = loop.run_until_complete(self.someOtherMethod())
        print('value from async func:', val)
        return val

@reloading
def main():
    MClass = myClass() # shit
    print(MClass)
    # breakpoint()
    val = A.someMethod()
    print('return value:', val)

    val = MClass.runAsync()
    print('return value:', val)
    # print('shit')
    print('good')

main()
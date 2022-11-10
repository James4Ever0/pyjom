from reloading import reloading
import asyncio


@reloading
class mClass:
    someValue = 2

    @reloading
    def someMethod(self):
        @reloading
        def someInnerMethod():
            raise Exception("exception1")
            return "inside function return"
        raise Exception("exception2")
        val = someInnerMethod()
        return val

    @reloading
    async def someOtherMethod(self):
        @reloading
        async def asyncInside():
            raise Exception("async exception2")
            return "async inside return"
        raise Exception('async exception1')
        val = await asyncInside()
        return val

    @reloading
    def runAsync(self):
        loop = asyncio.get_event_loop()
        val = loop.run_until_complete(self.someOtherMethod())
        print("value from async func:", val)
        return val


@reloading
def main():
    MClass = mClass()
    print(MClass)
    val = MClass.someMethod()
    print("return value:", val)
    val = MClass.runAsync()
    print("return async value:", val)
    print("success!")


main()

from reloading import reloading
import asyncio


# @reloading
class mClass:
    someValue = 2

    @reloading
    def someMethod(self):
        @reloading
        def someInnerMethod():
            raise Exception("inner exception")
            return "inside function return"
        raise Exception("exception")
        val = someInnerMethod()
        return val

    @reloading
    async def someOtherMethod(self):
        @reloading
        async def asyncInside():
            raise Exception("inner async exception")
            return "async inside return"
        raise Exception('async exception')
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

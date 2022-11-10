from reloading import reloading
import asyncio

# you had better decorate this.
# @reloading
class mClass:
    someValue = 2
    def forLoopInFunction(self):
        val='shit'
        # for i in reloading(range(3)): # still not solved!
        for i in range(3): # still not solved!
            # raise Exception('shit')
            # return in primary function, not here!
            if True:
                val = 'value'# value not assigned correctly.
                # break # break outside loop? fuck?
                # what the fuck?
        return val

    @reloading
    def someMethod(self):
        @reloading
        def someInnerMethod():
            # raise Exception("inner exception")
            return "inside function return"
        # raise Exception("exception")
        val = someInnerMethod()
        return val

    @reloading
    async def someOtherMethod(self):
        @reloading
        async def asyncInside():
            # raise Exception("inner async exception")
            return "async inside return"
        # raise Exception('async exception')
        val = await asyncInside()
        return val

    @reloading
    def runAsync(self):
        loop = asyncio.get_event_loop()
        val = loop.run_until_complete(self.someOtherMethod())
        print("value from async func:", val)
        return val

def forLoop():
    val = None
    for i in reloading(range(3)): # multiple reloading for for-loop is not supported.
        val = 'abcd'
    return val

@reloading
def main():
    MClass = mClass()
    print(MClass)
    val = MClass.someMethod()
    print("return value:", val)
    val = MClass.runAsync()
    print("return async value:", val)
    val = MClass.forLoopInFunction()
    print("return for loop value in class:", val)
    val = forLoop()
    print("return for loop value:", val)
    print("success!")


main()

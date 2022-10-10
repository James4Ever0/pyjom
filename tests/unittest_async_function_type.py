async def randomFunction():
    return 1
async def randomFunctionGenerator():
    yield await randomFunction()
from bilibili_api import sync
import types
type0=  type(randomFunction)
type1 = type(randomFunction())
type2 = types.AsyncGeneratorType
type3 = type(randomFunctionGenerator())
type4 = types.CoroutineType
type5 = type(randomFunctionGenerator)
print(type0, type1, type2, type3, type4, type5)
print(type1== type4)
print(type2 == type3)
# async generator can only be used for 
data = randomFunctionGenerator() # this is async generator. different!
data = sync(data)
# not good.
print(type(data))
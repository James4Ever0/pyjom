from reloading import reloading

# decorate here!
# @dec # won't fix here.
# @someRandomDecorator
@reloading # it won't help with everything.
def someFunction (a,b,c,d=1,f=2
):
    # not touching this function!
    # @decorator
    # def inner_function (h,i,j,
    # k):
    abcdefg=1234
    #     return hjkl
    return abcdefg # I need you to decorate this thing.

async def shitfunction():
    return shit

if __name__ == "__main__":
    someFunction(1,2,3)
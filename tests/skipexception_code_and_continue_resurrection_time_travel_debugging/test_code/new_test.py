from reloading import reloading

# decorate here!
@dec
@someRandomDecorator
@reloading
def someFunction (a,b,c,d=1,f=2
):
    # not touching this function!
    @decorator
    def inner_function (h,i,j,
    k):
        return hjkl
    return abcdefg # I need you to decorate this thing.

async def shitfunction():
    return shit

if __name__ == "__main__":
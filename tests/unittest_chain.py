import chain

@chain
def func(context, a,b):
    print(a,b)

chain.state() >> func(1,2) >> func(2,3) >> func(3,4)
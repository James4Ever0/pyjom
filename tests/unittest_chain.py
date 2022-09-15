import chain

@chain
def func(context, a,b):
    print(a,b)

chain.state() >> func >> func
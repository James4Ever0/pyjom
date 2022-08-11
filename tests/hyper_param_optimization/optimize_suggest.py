from hyperopt import tpe, fmin, hp
def function (x):
    print("")
    result = x**2
space = hp.uniform(0,2)
result = fmin(function, space=space, algo=tpe.suggest, max_evals=100)

print(result)
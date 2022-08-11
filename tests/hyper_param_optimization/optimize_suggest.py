from hyperopt import tpe, fmin, hp

result = fmin(function, space=space, algo=tpe.suggest, max_evals=100)
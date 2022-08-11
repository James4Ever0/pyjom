#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hyperopt import hp

# usually this hyper parameter optimization is done regularlly, and the optimized parameters will be used for a while till next update.
# but can we optimize these parameters offline?
# if not offline then we can only use traditional machine learning instead...

# or this trial and error process is actually a kind of offline machine learning, like random search and graph inference...

# better use hyperopt with a discriminator ML algorithm.

# space = hp.choice(
#     "a",
#     [("case 1", 1 + hp.lognormal("c1", 0, 1)), ("case 2", hp.uniform("c2", -10, 10))],
# )
import hyperopt.pyll.stochastic as stochastic

space = hp.choice("lambda",[lambda :1, lambda:2]) # if it is lambda, function will not resolve. however, after passing this thing into the main criterion function, it will utilize the lambda function.

for _ in range(10):
    sample = stochastic.sample(space)
    print("SAMPLE:", sample) # this will return the tuple. can we put some custom functions here?
    # there must be some integrations with custom functions. for example: scikit-learn

print("_______________________________") # splited.

from hyperopt.pyll import scope

@scope.define # this is how we sample the "LAMBDA".
def my_func(a,b=1):
    print("running function my_func", a,b)
    return a*b

space_0 = scope.my_func(hp.choice("myChoice",[1,2]))
space_1 = scope.my_func(hp.choice("myChoice",[1,2]), hp.choice("myChoice2",[2,3,4]))

for _ in range(10):
    print(stochastic.sample(space_0), stochastic.sample(space_1))
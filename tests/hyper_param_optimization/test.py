#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hyperopt import hp

space = hp.choice(
    "a",
    [("case 1", 1 + hp.lognormal("c1", 0, 1)), ("case 2", hp.uniform("c2", -10, 10))],
)

import hyperopt.pyll.stochastic as stochastic

for _ in range(10):
    sample = stochastic.sample(space)
from lazero.utils.tools import iteratorWrapper

sequence = [i for i in range(10)]

INIT_REPEAT=3
objective_init_repeat = sequence[0]*INIT_REPEAT + sequence

REPEAT = 2

objective_repeat = sequence[0]*INIT_REPEAT + []
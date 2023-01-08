from lazero.utils.tools import iteratorWrapper, flattenUnhashableList

sequence = [i for i in range(10)]

INIT_REPEAT=3
objective_init_repeat = [sequence[0]]*INIT_REPEAT + sequence

REPEAT = 2

objective_repeat = [sequence[0]]*INIT_REPEAT + flattenUnhashableList(list(zip(*([sequence]*REPEAT))))

MAX_ITER = 4

objective_max_iter = [sequence[0]]*INIT_REPEAT + flattenUnhashableList(list(zip(*([sequence[:MAX_ITER]]*REPEAT))))

def test_
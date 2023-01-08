from lazero.utils.tools import iteratorWrapper, flattenUnhashableList

sequence = [i for i in range(10)]

INIT_REPEAT=3
objective_init_repeat = [sequence[0]]*INIT_REPEAT + sequence

REPEAT = 2

objective_repeat = [sequence[0]]*INIT_REPEAT + flattenUnhashableList(list(zip(*([sequence]*REPEAT))))

MAX_ITER = 4

objective_max_iter = [sequence[0]]*INIT_REPEAT + flattenUnhashableList(list(zip(*([sequence[:MAX_ITER]]*REPEAT))))

def test_init_repeat():
    result = list(iteratorWrapper(sequence,init_repeat=INIT_REPEAT))
    assert result == objective_init_repeat


def test_repeat():
    result = list(iteratorWrapper(sequence,init_repeat=INIT_REPEAT,repeat=REPEAT))
    assert result == objective_repeat


def test_max_iter():
    result = list(iteratorWrapper(sequence,init_repeat=INIT_REPEAT,repeat=REPEAT,max_iter=MAX_ITER))
    assert result == objective_max_iter
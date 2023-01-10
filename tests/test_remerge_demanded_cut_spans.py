cut_spans = [(0,1),(1,2),(2,9),(9,100),(100,101),(101,102)]

from test_commons import *
from pyjom.lyrictoolbox import remergeDemandedCutSpans

def test_cut_spans_valid(list_of_spans, min_span=1.5, max_span=10,no_range_test=False):
    start = list_of_spans[0][0]
    init_end = list_of_spans[0][1]
    minit_duration = list_of_spans[0][1]-start
    if not no_range_test:
        assert start < list_of_spans[0][1]
        assert minit_duration >=min_span and minit_duration <=max_span
    # end = list_of_spans[-1][1]
    for span in list_of_spans[1:]:
        mstart, mend = span
        assert mstart == init_end
        assert mstart < mend
        duration = mend-mstart
        if not no_range_test:
            assert duration >=min_span and duration <= max_span
        init_end = mend

test_cut_spans_valid(cut_spans,no_range_test=True)
new_spans = remergeDemandedCutSpans(cut_spans)
print('new spans?',new_spans)
test_cut_spans_valid(new_spans)
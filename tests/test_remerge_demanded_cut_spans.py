cut_spans = [(0,1),(1,2),(2,9),(9,100),(100,101),(101,102)]

from import 
from pyjom.lyrictoolbox import remergeDemandedCutSpans

def test_cut_spans_valid(list_of_spans, min_span=1.5, max_span=10):
    start = list_of_spans[0][0]
    assert start < list_of_spans[0][1]
    minit_duration = list_of_spans[0][1]-start
    assert minit_duration >=min_span and minit_duration <=max_span
    # end = list_of_spans[-1][1]
    for span in list_of_spans[1:]:
        mstart, mend = span
        assert mstart < mend
        duration = mend-mstart
        assert duration >=min_span and duration <= max_span



new_spans = remergeDemandedCutSpans(cut_spans)
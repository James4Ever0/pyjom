cut_spans = [(0,1),(1,2),(2,9),(9,100),(100,101),(101,102)]

from import 
from pyjom.lyrictoolbox import remergeDemandedCutSpans

def test_cut_spans_valid(list_of_spans):
    start = list_of_spans[0][0]
    end = list_of_spans[-1][1]
    for span in list_of_spans:
        

new_spans = remergeDemandedCutSpans(cut_spans)
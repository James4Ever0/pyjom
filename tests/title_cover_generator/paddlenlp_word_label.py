from paddlenlp import  Taskflow
from commons import sample_data

# LAC 词语重要性

for elem in sample_data:
    flows = ["word_segmentation","ner","pos_tagging","dependency_parsing","information_extraction","sentiment_analysis","text_correction","knowledge_mining"]
    for flow in flows:
        if flow !="information_extraction":
            seg = Taskflow(flow) # need schema for information extraction.
        else:
            schema = ["主语","谓语","宾语"]
            seg = Taskflow(flow, schema=schema) # need schema for information extraction
        data = seg(elem)
        del seg
        print(flow,data)
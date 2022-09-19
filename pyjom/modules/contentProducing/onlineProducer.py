from pyjom.commons import *

@decorator
def OnlineProducer(processed_info, template=None, template_config={}):
    template_function = getProducerTemplate[template]
    template_function(processed_info,)
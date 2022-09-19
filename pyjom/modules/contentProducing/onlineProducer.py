from pyjom.commons import *

@decorator
def OnlineProducer(info, template=None, template_config={}):
    template_function = getProducerTemplate[template]
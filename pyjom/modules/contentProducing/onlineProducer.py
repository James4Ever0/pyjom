from pyjom.commons import *

@decorator
def OnlineProducer(info, template=None):
    template_function = getProducerTemplate
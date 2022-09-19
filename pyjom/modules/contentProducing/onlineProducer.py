from pyjom.commons import *
from pyjom.modules.contentProducing.producerTemplates import getProducerTemplate

@decorator
def OnlineProducer(processed_info, template=None, template_config={}):
    template_function = getProducerTemplate[template]
    exported_media_location = template_function(processed_info,config=template_config)
    # i guess the title/tags/cover are actually belongs to the poster, not 
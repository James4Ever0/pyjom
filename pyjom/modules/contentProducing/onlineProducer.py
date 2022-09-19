from pyjom.commons import *
from pyjom.modules.contentProducing.producerTemplates import getProducerTemplate

@decorator
def OnlineProducer(processed_info, source = 'giphy',template=None, template_config={}):
    if source == 'giphy':
        template_function = getProducerTemplate[template]
        exported_media_locations = template_function(processed_info,config=template_config) # a generator!
        # i guess the title/tags/cover are actually belongs to the poster, not producer.
        for exported_media_location in exported_media_locations:
            yield exported_media_location
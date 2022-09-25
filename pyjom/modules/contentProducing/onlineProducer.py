from pyjom.commons import *
from pyjom.modules.contentProducing.producerTemplates import getProducerTemplate

from lazero.filesystem.temp import tmpdir
@decorator
def OnlineProducer(processed_info_generator, source = 'giphy',template=None, template_configs=None, fast:bool=True, medialangTmpdirBase="/dev/shm/medialang"):
    # template_configs is a generator, it generate configs.
    # print("PROCESSED_INFO_GENERATOR: ", processed_info_generator)
    # breakpoint()
    import uuid
    with tmpdir(path=# must use another level of abstraction
    if source == 'giphy':
        template_function = getProducerTemplate(template)
        # print("TEMPLATE FUNCTION ACQUIRED %s" % template_function)
        # breakpoint()
        exported_media_locations = template_function(processed_info_generator,configs=template_configs, fast=fast) # a generator!
        # i guess the title/tags/cover are actually belongs to the poster, not producer.
        for exported_media_location in exported_media_locations:
            print('exported media location:', exported_media_location)
            breakpoint()
            yield exported_media_location
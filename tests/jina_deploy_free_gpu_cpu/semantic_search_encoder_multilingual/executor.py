from jina import Executor, DocumentArray, requests
import numpy as np

from txtai.embeddings import Embeddings

class semantic_search_encoder_multilingual(Executor):
    embeddings = Embeddings({
            "path": "sentence-transformers/distiluse-base-multilingual-cased-v1"
        } )
    @requests
    def foo(self, docs: DocumentArray, **kwargs):
        try:
            command = docs[0].text
            command = command.strip()
            if len(command) == 0:
                raise Exception('No command')
            response = self.embeddings.transform((None, command, None))
            response = np.array([response])
            docs[0].data = response
            docs[0].msg = 'success'
        # docs[1].text = 'goodbye, world!'
        except:
            import traceback
            error = traceback.format_exc()
            docs[0].data = None
            docs[0].msg = "\n".join(["error!", error])

from jina import Executor, DocumentArray, requests
import numpy as np

from txtai.embeddings import Embeddings


#     raise RuntimeError(
# RuntimeError: Cannot re-initialize CUDA in forked subprocess. To use CUDA with multiprocessing, you must use the 'spawn' start method

class semantic_search_encoder_multilingual(Executor):
    embeddings = Embeddings({
            "path": "sentence-transformers/distiluse-base-multilingual-cased-v1"
        } )
    @requests
    def foo(self, docs: DocumentArray, **kwargs):
        try:
            command = docs[0].text
            command = command.strip()
            if len(command) == 0 or command == '_success':
                raise Exception('No command')
            response = self.embeddings.transform((None, command, None))
            response = np.array([response])
            docs[0].embedding = response
            docs[0].text = '_success'
        # docs[1].text = 'goodbye, world!'
        except:
            import traceback
            error = traceback.format_exc()
            print(error)
            docs[0].embedding = None
            docs[0].text = "\n".join(["error!", error])

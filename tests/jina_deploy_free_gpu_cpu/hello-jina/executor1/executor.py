from jina import Executor, requests, DocumentArray
# remember our good old program? our shell?
# proper name is: reverse shell
# hackish? no?

import subprocess

class MyExecutor(Executor):
    @requests
    def foo(self, docs: DocumentArray, **kwargs):
        docs[0].text = 
        docs[0].text = response
        # docs[1].text = 'goodbye, world!'

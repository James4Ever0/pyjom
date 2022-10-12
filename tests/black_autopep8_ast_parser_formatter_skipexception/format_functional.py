with open("test.py", "r") as f:
    code = f.read()

# need binary data.
code_encoded = code.encode("utf-8")

import subprocess

MAXINT = 10000000000
command = "autopep8 --max-line-length {MAXINT} - | black -l {MAXINT} -C -".format(
    MAXINT=MAXINT
)
commandLine = ["bash", "-c", command]
result = subprocess.run(commandLine, input=code_encoded, capture_output=True)
try:
    assert result.returncode == 0
    code_formatted = result.stdout.decode("utf-8")
except:
    import traceback

    traceback.print_exc()
    print("STDOUT", result.stdout)
    print("STDERR", result.stderr)
    code_formatted = code

print(code_formatted)

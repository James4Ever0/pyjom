# view only. no change on original content.
MAXINT=1000000
cat test.py | autopep8 --max-line-length $MAXINT - | black -l $MAXINT -C - 2>/dev/null
# view only. no change on original content.
MAXINT=10000000
cat test.py | autopep8 --max-line-length $MAXINT | black -l $MAXINT -C
# view only. no change on original content.
# of course, for lines with long content, we will have trouble.
MAXINT=1000000000
cat test.py | autopep8 --max-line-length $MAXINT - | black -l $MAXINT -C - 2>/dev/null
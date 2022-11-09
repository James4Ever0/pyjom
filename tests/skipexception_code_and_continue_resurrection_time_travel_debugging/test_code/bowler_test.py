import bowler

src ='test2.py'

pattern="""(
    decorated=decorated<
        decorators=decorators
        function_def=funcdef<
            'def' function_name=funcname
            function_parameters=parameters< '(' function_arguments=any* ')' >
            any*
        >
    >
|
    function_def=funcdef<
        'def' function_name=funcname
        function_parameters=parameters< '(' function_arguments=any* ')' >
        any*
    >
)"""

q = bowler.Query(src)
f = q.select(pattern)
# print(f, dir(f))
for x in f:
    print(x)
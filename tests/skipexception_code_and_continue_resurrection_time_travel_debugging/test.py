def troubleFunction():
    a = 0
    print(b) # skipped
    return b # also skipped
    return a # successfully returned with value of a

val = troubleFunction()
print(val) # 0

c = 0
print(d) # skipped
print(c) # printing value of c
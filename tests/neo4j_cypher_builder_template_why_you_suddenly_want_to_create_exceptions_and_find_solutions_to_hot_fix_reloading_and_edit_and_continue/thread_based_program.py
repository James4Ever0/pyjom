import threading

event = threading.Event()
event.clear()

# is it event driven? can we launch repl after this?
def program(*args): # in elixir/erlang this is simpler.
    print('running program')
    while True:
        if event.wait(0.00000001):
            break # this is blocking. fuck. not like elixir in any kind.
        else:
            event.set()
    event.clear()
    print('begin execution')
    print("arguments:", args)
    raise Exception('shit man')
    event.set()
    result = 'myresult'

def mainThread():
    threading.Thread(target=program, args=(1,2), daemon=True).start()
    print('waiting output? probably never.')
    while True:
        if event.wait(0.00000001):
            break # are you sure this is the event you want?
        else:
            event.set()
    print('result:',result) # another thread? are you sharing things?
    print('main thread execution succeed')

print('starting main thread')
threading.Thread(target=mainThread, daemon=True).run()
print('starting repl')
# be ready to re-execute the program?
# do you want something like nodejs promises?
# how to reload foreign files? fuck?
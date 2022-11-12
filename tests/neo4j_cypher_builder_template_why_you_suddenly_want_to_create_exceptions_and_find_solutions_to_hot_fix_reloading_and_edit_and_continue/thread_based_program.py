import threading

event = threading.Event()
event.clear()

# is it event driven? can we launch repl after this?
def program(*args): # in elixir/erlang this is simpler.
    event.wait()
    event.clear()
    print('begin execution')
    print("arguments:", args)
    raise Exception('shit man')
    event.set()
    result = 'myresult'

def mainThread():
    threading.Thread(target=program, args=(1,2), daemon=True).start()
    print('waiting output? probably never.')
    result = event.wait() # are you sure this is the event you want?
    print('result:',result)
    print('main thread execution succeed')

print('starting main thread')
threading.Thread(target=mainThread, daemon=True).start()
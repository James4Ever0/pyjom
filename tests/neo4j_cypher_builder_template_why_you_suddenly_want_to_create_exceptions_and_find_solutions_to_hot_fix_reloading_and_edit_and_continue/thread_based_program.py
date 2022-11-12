import threading
event = threading.Event()
event.clear()
def program(*args): # in elixir/erlang this is simpler.
    event.wait()
    event.clear()
    print('begin execution')
    print("arguments:", args)
    raise Exception('shit man')
    event.set()
    result = 'myresult'

threading.Thread(target=program, args=(1,2))
print('waiting output? probably never.')
result = event.wait()
print('result:',result)
import threading

def program(*args): # in elixir/erlang this is simpler.
    print("arguments:", args)
    raise Exception('shit man')
    result = 'myresult'

threading.Thread(target=program, args=(1,2))
result = threading.Event()
print('result:',result)
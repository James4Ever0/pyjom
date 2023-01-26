from pynput.keyboard import Key, Listener
  
def on_press(key):
     
    keys.append(key)
     
    try:
        print('alphanumeric key {0} pressed'.format(key.char))
    except AttributeError:
        print('special key {0} pressed'.format(key))
          
def on_release(key):
                     
    print('{0} released'.format(key))
    if key == Key.esc:
        # Stop listener
        return False
                     

listener = Listener(on_press = on_press,
              on_release = on_release)
# listener.start()
with listener:
    listener.join()
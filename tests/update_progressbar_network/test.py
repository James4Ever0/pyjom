# try to update progressbar via network.

from tqdm import tqdm
t = None
def hello():

def close_progressbar():
    global t
    if t is not None:
        try:
            t.close()
        except:
            import traceback
            traceback.print_exc()
            print('error resetting progressbar')

def reset(): # pass the iteration count
    global t

    t = tqdm(total=total)

def update_progressbar():
    t.update(progress)

def close():

# try to update progressbar via network.
from typing import Union

from fastapi import FastAPI

app = FastAPI()

from tqdm import tqdm

t = None


def hello():

# not routing this to network.
def close_progressbar():
    global t
    if t is not None:
        try:
            t.close()
        except:
            import traceback
            traceback.print_exc()
            print('error closing progressbar')

def reset(): # pass the iteration count
    global t
    close_progressbar()
    t = tqdm(total=total)

def update_progressbar():
    t.update(progress)

def close():
    close_progressbar()

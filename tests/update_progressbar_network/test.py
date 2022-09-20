# try to update progressbar via network.
from typing import Union

from fastapi import FastAPI

app = FastAPI()

from tqdm import tqdm

t = None

@app.get('/')
def hello():
    return 'progressbar server'

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

@app.get('/reset')
def reset(total: int): # pass the iteration count
    global t
    close_progressbar()
    t = tqdm(total=total)

@app.get('/update')
def update_progressbar(progress: int):
    global t
    if t is not None:
    try:
        t.update(progress)
    except:

@app.get('/close')
def close():
    close_progressbar()

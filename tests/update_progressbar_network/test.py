# try to update progressbar via network.
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
            return {'msg':'success'}
        except:
            import traceback
            traceback.print_exc()
            print('error closing progressbar')
            return {'msg':'error closing progressbar'}

@app.get('/reset')
def reset(total: int, name:str='random task'): # pass the iteration count
    global t
    close_progressbar()
    print('processing:', name)
    t = tqdm(total=total)
    return {'msg':'success'}

@app.get('/update')
def update_progressbar(progress: int=1):
    global t
    if t is not None:
        try:
            t.clear()
            t.update(progress)
            return {'msg':'success'}
        except:
            import traceback
            traceback.print_exc()
            print("error when updating progessbar")
            return {'msg':'error when updating progessbar'}
    else:
        print('no progressbar available')
        return {'msg':'no progressbar available'}


@app.get('/close')
def close():
    close_progressbar()
    return {'msg':'success'}

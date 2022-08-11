from hyperopt import tpe, fmin, hp, STATUS_OK, STATUS_FAIL
import requests
def function(x):
    print("calculating function...",x)
    # result = x**2
    status = STATUS_FAIL
    try:
        r = requests.get('https://www.baidu.com/', timeout=x)
        if r.status_code == 200:
            status = STATUS_OK
    return {"loss":x, "status":status}
space = hp.uniform("param",1,2)
result = fmin(fn=function, space=space, algo=tpe.suggest, max_evals=100)

print(result)
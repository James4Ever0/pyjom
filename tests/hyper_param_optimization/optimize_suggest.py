from hyperopt import tpe, fmin, hp, STATUS_OK, STATUS_FAIL
import requests
def function(x):
    print("trying timeout:",x)
    # result = x**2
    status = STATUS_FAIL
    try:
        r = requests.get('https://www.baidu.com/', timeout=x)
        if r.status_code == 200:
            status = STATUS_OK
    except:
        print("FAILED WITH TIMEOUT:", x) # this will rule out the unwanted ones.
    return {"loss":x, "status":status}
space = hp.uniform("param",0,2)
result = fmin(fn=function, space=space, algo=tpe.suggest, max_evals=100)

print(result)
# {'param': 0.10165862536290635}
# really working? 100ms could be so damn short...

# by using `Trials` we could inspect results of every trial.
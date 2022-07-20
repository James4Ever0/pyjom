import json


def jsonWalk(jsonObj,location=[]):
    # this is not tuple. better convert it first?
    # mlocation = copy.deepcopy(location)
    if type(jsonObj) == dict:
        for key in jsonObj:
            content = jsonObj[key]
            if type(content) not in [dict,list,tuple]: 
                yield location+[key], content
            else:
                # you really ok with this?
                for mkey, mcontent in jsonWalk(content,location+[key]):
                    yield mkey, mcontent
    elif type(jsonObj) in [list,tuple]:
        for key,content in enumerate(jsonObj):
        # content = jsonObj[key]
            if type(content) not in [dict,list,tuple]:
                yield location+[key], content
            else:
                for mkey, mcontent in jsonWalk(content,location+[key]):
                    yield mkey, mcontent
    else:
        raise Exception("Not a JSON compatible object: {}".format(type(jsonObj)))

def jsonLocate(jsonObj,location=[]):
    # print("object:",jsonObj)
    # print("location:",location)
    if location!=[]:
        return jsonLocate(jsonObj[location[0]],location[1:])
    return jsonObj

json.__dict__.update({"walk":jsonWalk,"locate":jsonLocate})


def list_startswith(a,b):
    value = 0
    if len(a) < len(b): return False
    for i,v in enumerate(b):
        v0 = a[i]
        if v == v0:
            value +=1
    return value == len(b)

def list_endswith(a,b):
    value = 0
    if len(a) < len(b): return False
    c = a[-len(b):]
    for i,v in enumerate(b):
        v0 = c[i]
        if v == v0:
            value +=1
    return value == len(b)


# list.__dict__.update({"startswith": list_startswith,"endswith": list_endswith})


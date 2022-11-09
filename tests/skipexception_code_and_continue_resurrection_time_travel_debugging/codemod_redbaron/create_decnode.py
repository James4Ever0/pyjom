import redbaron

def getd():
    code="""@abcd
    def shit(): pass"""
    d=redbaron.RedBaron(code)[0].decorators[0]
    #print(d,type(d))
    return d


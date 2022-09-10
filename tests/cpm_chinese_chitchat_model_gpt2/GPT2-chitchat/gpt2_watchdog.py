import requests
import schedule
def getNow():
    return datetime.datetime.now()
    
def getGPT2Status():
    hour = getNow().hour
    if hour > 2 and hour < 8:
        return 'train'
    else:
        return 'eval'

def getGPT2TrainedStatus():
    try:
        with open('trained.log', 'r+') as f:
            content = f.read()
        content = datetime.datetime.fromisoformat(content)
        day = content.day
        now = getNow()
        return day == now.day
    except:
        import traceback
        traceback.print_exc()
        print("SOME ERROR WHEN CHECKING GPT2 TRAINED STATUS")
        breakpoint()
    return False

import os
def startGPT2Training():
    os.chdir("/root/Desktop/works/pyjom/tests/cpm_chinese_chitchat_model_gpt2/GPT2-chitchat/")
    os.system('python3 ')
def checkGPT2Status():
    gpt2status = getGPT2Status()
    if gpt2status == 'train':
        trained = getGPT2TrainedStatus()
        if not trained:
            startGPT2Training()
            markGPT2Trained()
        else:
            print("GPT2 is Trained Today.")
    elif gpt2status == 'eval':
        running = getGPT2Running()
        if not running:
            startGPT2Server()
        else:
            print("GPT2 is running...")

schedule.every(1).minute.do(checkGPT2Status) # shall place a flag if the training is complete.
# schedule.every(1).minute.do(checkGPT2TrainServer)
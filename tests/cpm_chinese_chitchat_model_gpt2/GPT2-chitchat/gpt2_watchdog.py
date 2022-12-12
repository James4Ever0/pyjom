import requests
import schedule
import os
import datetime

os.chdir(
    "/root/Desktop/works/pyjom/tests/cpm_chinese_chitchat_model_gpt2/GPT2-chitchat/"
)


def getNow():
    return datetime.datetime.now()

# fuck! if you disable this, you must clean our cache of talks!
def getGPT2Status(start=0, end=1, force_eval:bool=False): # how about disable the training capability? since that eats our VRAM.
    # but again, while training, gpt2 is offline and the bot might be on some inconsistent state, luring the administrator to remove our bot.
    # if you want to write unit tests for your video making app, this is the time.
    if force_eval:
        return 'eval'
    hour = getNow().hour
    print("HOUR: ", hour)
    # if hour >= 16 and hour <= 20: # for test
    # if hour >= 2 and hour <= 8:
    if hour >= start and hour <= end:  # for practice?
    # if hour >= 21 and hour <= 22:  # for practice
        return "train"
    else:
        return "eval"


def getGPT2TrainedStatus():
    try:
        with open("trained.log", "r+") as f:
            content = f.read()
        content = datetime.datetime.fromisoformat(content)
        day = content.day
        now = getNow()
        return day == now.day
    except:
        import traceback

        traceback.print_exc()
        print("SOME ERROR WHEN CHECKING GPT2 TRAINED STATUS")
        # breakpoint()
    return False


# import os
def startGPT2Training():
    print("START TRAINING")
    # acquire the lock.
    import filelock
    with filelock.FileLock("model_training.lock", timeout=5): # you may have problems.
        os.system("/usr/bin/python3 train_model_fastapi.py")


def markGPT2Trained():
    with open("trained.log", "w+") as f:
        content = getNow().isoformat()
        f.write(content)
    print("GPT2 TRAINED STATUS MARKED")


import subprocess

process = None


def getGPT2Running():
    global process
    if process != None:
        return process.poll() == None  # when no return code the program is running
    return False  # if process is None then program is not running


def startGPT2Server():
    global process
    process = subprocess.Popen(
        ["/usr/bin/python3", "interact_fastapi.py", "--model_path", "../model"]
    )
    # process.poll()


def terminateGPT2():
    global process
    if process:
        try:
            process.terminate()
            print("GPT2 SERVER TERMINATED")
        except:
            import traceback

            traceback.print_exc()
            print("ERROR WHEN TERMINATING GPT2 SERVER")
            breakpoint()
    else:
        print("GPT2 IS NOT RUNNING. NO NEED TO TERMINATE")


def checkGPT2Status():
    gpt2status = getGPT2Status()
    print("gpt2 status: " + gpt2status)
    if gpt2status == "train":
        terminateGPT2()
        trained = getGPT2TrainedStatus()
        if not trained:
            startGPT2Training()
            markGPT2Trained()
        else:
            print("GPT2 is Trained Today.")
    elif gpt2status == "eval":
        running = getGPT2Running()
        if not running:
            startGPT2Server()
        else:
            print("GPT2 is running...")


schedule.every(1).minute.do(
    checkGPT2Status
)  # shall place a flag if the training is complete.
# schedule.every(1).minute.do(checkGPT2TrainServer)

import time

if __name__ == "__main__":
    checkGPT2Status()
    while True:
        time.sleep(10)
        schedule.run_pending()

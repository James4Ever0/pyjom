import requests
import schedule
import os
import datetime

os.chdir(
    "/root/Desktop/works/pyjom/tests/cpm_chinese_chitchat_model_gpt2/GPT2-chitchat/"
)


def getNow():
    return datetime.datetime.now()


def getGPT2Status():
    hour = getNow().hour
    if hour > 2 and hour < 8:
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
        breakpoint()
    return False


# import os
def startGPT2Training():
    print("START TRAINING")
    os.system("/usr/bin/python3 train_model_fastapi.py")


def markGPT2Trained():
    with open("trained.log", "r+") as f:
        content = getNow().isoformat()
        f.write(content)
    print("GPT2 TRAINED STATUS MARKED")


import subprocess

process = None


def getGPT2Running():
    global process
    returnCode = process.poll()
    return process != None


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

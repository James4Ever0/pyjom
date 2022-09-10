import requests
import schedule

schedule.every(1).minute.do(checkGPT2Status)
# schedule.every(1).minute.do(checkGPT2TrainServer)
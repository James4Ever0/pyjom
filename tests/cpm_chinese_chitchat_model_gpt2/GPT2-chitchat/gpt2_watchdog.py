import requests
import schedule

schedule.every(1).minute.do(checkGPT2EvalServer)
schedule.every(1).minute.do(checkGPT2TrainServer)
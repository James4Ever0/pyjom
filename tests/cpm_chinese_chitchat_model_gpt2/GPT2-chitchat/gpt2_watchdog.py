import requests
import schedule

schedule.every(1).minute.do(checkGPT2Server)
schedule.every(1).minute.do(checkGPT2Server)
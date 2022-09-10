import requests
import schedule

schedule.every(1).minute.do(check)
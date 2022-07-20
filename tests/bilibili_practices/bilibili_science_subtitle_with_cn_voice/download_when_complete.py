import parse
import subprocess
import time
import os
# import pathlib

download_lock = ".kaggle_downloaded"

if os.path.exists(download_lock):
    print("already fetched content.")

wait_duration = 60

formatx = '{a} has status "{b}"'
valid_status = ["running","complete"]

final_command = "kaggle kernels output jessysisca/test-of-yt-dlp2"
cmd = "kaggle kernels status jessysisca/test-of-yt-dlp2"

while True:
    output = subprocess.check_output(cmd.split(" "))
    output = output.decode('utf-8')
    output = output.replace('\n',"").strip()

    result = parse.parse(formatx,output)

    rb = result['b']

    print("STATUS:",rb)
    if rb in valid_status:
        if rb == "complete":
            print("DOWNLOADING OUTPUT")
            os.system(final_command)
            os.system("touch {}".format(download_lock))
            break
        else:
            time.sleep(wait_duration)
    else:
        print("UNKNOWN STATUS. ERROR.")
        break
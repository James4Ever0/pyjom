cd ../GPT2-chitchat
# there is no argparse support.
# python3 -m uvicorn interact_fastapi:app --reload --port 8932 

# python3 interact_fastapi.py --model_path ../model # use cuda somehow, checking if that saves my cpu?
python3 gpt2_watchdog.py

# but that will not work for yolov5 detection.
# anyway i am trying to be economic.
#python3 interact_fastapi.py --no_cuda --model_path ../model

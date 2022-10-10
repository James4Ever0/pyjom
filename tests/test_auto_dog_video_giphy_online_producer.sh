# env LD_LIBRARY_PATH=/usr/local/lib python3 test_auto_dog_video_giphy_online_producer.py 

#### PHASE 1 ####
# FULL TEST
ulimit -n 1048576 # to avoid NOF issues.
tmux kill-session -t online_dog_cat_generator_test && echo "killed session: online_dog_cat_generator_test"
tmuxp load test_auto_dog_video_giphy_online_producer.yaml

#### PHASE 2 ####
# check medialang render result.
# python3 test_auto_dog_video_giphy_online_producer.py -p
# seems all good. but the time duration is not so good. maybe gaussian will help? set breakpoint after main list is created.
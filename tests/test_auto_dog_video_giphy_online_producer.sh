# env LD_LIBRARY_PATH=/usr/local/lib python3 test_auto_dog_video_giphy_online_producer.py 
tmux kill-session -t online_dog_cat_generator_test && echo "killed session: online_dog_cat_generator_test"
tmuxp load test_auto_dog_video_giphy_online_producer.yaml
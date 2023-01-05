cd /root/Desktop/works/pyjom/tests/
python3 launch_test_enviroment.py

# # launch bilibili recommendation server
# cd /root/Desktop/works/pyjom/tests/bilibili_video_recommendation_server
# gnome-terminal -- python3 /root/Desktop/works/pyjom/tests/bilibili_video_recommendation_server/test.py

# # launch qq cqhttp
# cd /root/Desktop/works/pyjom/tests/qq_go_cqhttp
# gnome-terminal -- bash /root/Desktop/works/pyjom/tests/qq_go_cqhttp/launch.sh

# # make sure milvus is running.
# cd /root/Desktop/works/pyjom/tests/video_phash_deduplication/
# bash /root/Desktop/works/pyjom/tests/video_phash_deduplication/config_milvus.sh

# # launch netease api server. we need it to download new music, currently.
# # video phash is the last step among all filters.
# cd /root/Desktop/works/pyjom/externals/NeteaseCloudMusicApi
# gnome-terminal -- bash /root/Desktop/works/pyjom/externals/NeteaseCloudMusicApi/launch.sh # port is 4042. port 4000 is used. don't know why.

# # how to check avaliability of netease cloud music api?

# cd /root/Desktop/works/pyjom/tests/karaoke_effects/
# gnome-terminal -- bash /root/Desktop/works/pyjom/tests/karaoke_effects/load_translator.sh

# sleep 1
# cd /root/Desktop/works/pyjom/tests/redis_music_info_persistance
# gnome-terminal -- bash /root/Desktop/works/pyjom/tests/redis_music_info_persistance/launch_redis.sh

# sleep 1
# cd /root/Desktop/works/pyjom/tests/random_giphy_gifs/
# gnome-terminal -- node /root/Desktop/works/pyjom/tests/random_giphy_gifs/nodejs_server.js

# sleep 1
# cd /root/Desktop/works/pyjom/tests/nsfw_violence_drug_detection
# gnome-terminal -- node /root/Desktop/works/pyjom/tests/nsfw_violence_drug_detection/nsfwjs_test.js
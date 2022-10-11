# launch netease api server. we need it to download new music, currently.

cd /root/Desktop/works/pyjom/tests/karaoke_effects/
gnome-terminal -- bash /root/Desktop/works/pyjom/tests/karaoke_effects/load_translator.sh

sleep 1
cd /root/Desktop/works/pyjom/tests/redis_music_info_persistance
gnome-terminal -- bash /root/Desktop/works/pyjom/tests/redis_music_info_persistance/launch_redis.sh

sleep 1
cd /root/Desktop/works/pyjom/tests/random_giphy_gifs/
gnome-terminal -- node /root/Desktop/works/pyjom/tests/random_giphy_gifs/nodejs_server.js

sleep 1
cd /root/Desktop/works/pyjom/tests/nsfw_violence_drug_detection
gnome-terminal -- node /root/Desktop/works/pyjom/tests/nsfw_violence_drug_detection/nsfwjs_test.js
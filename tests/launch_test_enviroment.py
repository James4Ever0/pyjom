import time
import os

def launchProgramWithTerminal(directory, intepreter,executable, sleep=None, no_terminal=False):
    try:
        if sleep:
            time.sleep(sleep)
        directory = os.path.abspath(directory)
        assert os.path.exists(directory)
        os.chdir(directory)
        executable_path = os.path.join(directory, executable)
        assert os.path.exists(executable_path)
        command = f'{"gnome-terminal -- " if not no_terminal else ""}{intepreter} {executable_path}'
        print('executing command:', command)
        os.system(command)
    except:
        import traceback
        traceback.print_exc()
        print('failed while launching program with parameters:')
        print(f"[D]:{directory}\n[I]{intepreter}\n[E]{executable}\n[C]{dict(sleep=sleep, no_terminal=no_terminal)}")
        breakpoint()

pyjom_directory = "/root/Desktop/works/pyjom/"

# launch billibili recommendation server
["/root/Desktop/works/pyjom/tests/bilibili_video_recommendation_server","python3","test.py"],{}

# launch qq cqhttp
["/root/Desktop/works/pyjom/tests/qq_go_cqhttp","bash","launch.sh"],{}

# make sure milvus is running.
["/root/Desktop/works/pyjom/tests/video_phash_deduplication/","bash","config_milvus.sh",dict(no_terminal=True)

# launch netease api server. we need it to download new music, currently.
# video phash is the last step among all filters.
["/root/Desktop/works/pyjom/externals/NeteaseCloudMusicApi",
"bash","launch.sh"],{} # port is 4042. port 4000 is used. don't know why.

# how to check avaliability of netease cloud music api?

["/root/Desktop/works/pyjom/tests/karaoke_effects/","bash","load_translator.sh"]

["/root/Desktop/works/pyjom/tests/redis_music_info_persistance","bash", "launch_redis.sh"],dict(sleep=1)


["/root/Desktop/works/pyjom/tests/random_giphy_gifs/","node","nodejs_server.js"],dict(sleep=1)


["/root/Desktop/works/pyjom/tests/nsfw_violence_drug_detection","node","nsfwjs_test.js"],dict(sleep=1)
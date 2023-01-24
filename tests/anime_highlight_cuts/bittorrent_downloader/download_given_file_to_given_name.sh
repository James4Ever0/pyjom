# how to end downloading when finished?
# using some command?
BASE_PATH="/Users/jamesbrown/Downloads/anime_download"
# DOWNLOAD_FILE_PATH="$BASE_PATH/sample.webp"
TORRENT_PATH="$BASE_PATH/[Kamigami&VCB-Studio] Yahari Ore no Seishun Lovecome wa Machigatte Iru. [Ma10p_1080p].torrent"
echo "ps aux | grep sample.webp | grep -v grep | awk '{print \$1}' | xargs -Iabc kill -s INT abc" > kill_aria2c.sh
FILE_ID="117"
# timeout set to what?
# rm "$DOWNLOAD_FILE_PATH"
# this will be ignored.

aria2c -x 16 --select-file="$FILE_ID" --on-download-complete "bash kill_aria2c.sh" --file-allocation=none "$TORRENT_PATH" 
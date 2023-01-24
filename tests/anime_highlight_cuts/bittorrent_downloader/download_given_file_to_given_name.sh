# how to end downloading when finished?
# using some command?
BASE_PATH="/Users/jamesbrown/Downloads/anime_download"
# DOWNLOAD_FILE_PATH="$BASE_PATH/sample.webp"
TORRENT_NAME="[Kamigami&VCB-Studio] Yahari Ore no Seishun Lovecome wa Machigatte Iru. [Ma10p_1080p]"
# torrent name might be different.
TORRENT_PATH="$BASE_PATH/$TORRENT_NAME.torrent"
# echo "ps aux | grep '$TORRENT_NAME' | grep -v grep | awk '{print \$1}' | xargs -Iabc kill -s INT abc" > kill_aria2c.sh
FILE_ID="117"

# timeout set to what?
# rm "$DOWNLOAD_FILE_PATH"
rm -rf "$TORRENT_NAME"
rm -rf "$TORRENT_NAME.aria2"
# this will be ignored.

# change directory to our temp directory.

# this speed shall be precalculated.
# 

# you may check integrity.

# just count seeders.

# aria2c -x 16 --select-file="$FILE_ID" --seed-time=0 --file-allocation=none "$TORRENT_PATH"
# aria2c -x 16 --select-file="$FILE_ID" --seed-time=0 --file-allocation=none --lowest-speed-limit=300K --bt-stop-timeout=60 "$TORRENT_PATH"
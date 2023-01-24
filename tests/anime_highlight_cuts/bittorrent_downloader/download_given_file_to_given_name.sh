# how to end downloading when finished?
# using some command?
BASE_PATH=""
DOWNLOAD_FILE_PATH=""
TORRENT_PATH=""
echo "" > kill_aria2c.sh
aria2c -x 16 --on-download-complete "bash kill_aria2c.sh" --file-allocation=none "$TORRENT_PATH" 
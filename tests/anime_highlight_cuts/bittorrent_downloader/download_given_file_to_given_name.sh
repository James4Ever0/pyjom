# how to end downloading when finished?
# using some command?
BASE_PATH=""
DOWNLOAD_FILE_PATH=""
TORRENT_PATH=""

aria2c -x 16 --on-download-complete "" --file-allocation=none "$TORRENT_PATH" 
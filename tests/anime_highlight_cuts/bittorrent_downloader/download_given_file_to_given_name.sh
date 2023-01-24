# how to end downloading when finished?
# using some command?
BASE_PATH="/Users/jamesbrown/Downloads/anime_download"
DOWNLOAD_FILE_PATH="$BASE_PATH/"
TORRENT_PATH="$BASE_PATH/[Kamigami&VCB-Studio] Yahari Ore no Seishun Lovecome wa Machigatte Iru. [Ma10p_1080p].torrent"
echo "" > kill_aria2c.sh
aria2c -x 16 --on-download-complete "bash kill_aria2c.sh" --file-allocation=none "$TORRENT_PATH" 
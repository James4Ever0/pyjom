torrent_path = "/Users/jamesbrown/Downloads/anime_download/[Kamigami&VCB-Studio] Yahari Ore no Seishun Lovecome wa Machigatte Iru. [Ma10p_1080p].torrent"

import WebTorrent from 'webtorrent'

const client  = new WebTorrent()

client.add(torrent_path,torrent =>{
    torrent.files.
})
torrentPath = "/Users/jamesbrown/Downloads/anime_download/[Kamigami&VCB-Studio] Yahari Ore no Seishun Lovecome wa Machigatte Iru. [Ma10p_1080p].torrent"

// require_esm =require('esm')(module)
// const{WebTorrent} = require_esm('webtorrent').default
import ffmpeg from 'fluent-ffmpeg.js'
import WebTorrent from 'webtorrent.js'
// const WebTorrent =await import('webtorrent')
console.log("WEBTORRENT OBJECT?",WebTorrent)
const client = WebTorrent()

client.add(torrentPath,torrent =>{
    var selectedFiles = torrent.files.find(file =>{
        console.log("FILENAME?", file.name)
        return file.name.endswith('.mkv')
    })
    console.log("SELECTED FILES?")
    console.log(selectedFiles)
})
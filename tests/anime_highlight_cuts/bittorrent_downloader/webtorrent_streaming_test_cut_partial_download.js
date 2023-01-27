torrentPath = "/Users/jamesbrown/Downloads/anime_download/[Kamigami&VCB-Studio] Yahari Ore no Seishun Lovecome wa Machigatte Iru. [Ma10p_1080p].torrent"

require =require('esm')(module)
const{WebTorrent} = require('webtorrent').default

const client = new WebTorrent()

client.add(torrentPath,torrent =>{
    var selectedFiles = torrent.files.find(file =>{
        console.log("FILENAME?", file.name)
        return file.name.endswith('.mkv')
    })
    console.log("SELECTED FILES?")
    console.log(selectedFiles)
})
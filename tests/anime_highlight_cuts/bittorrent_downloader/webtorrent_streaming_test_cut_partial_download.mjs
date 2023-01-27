var torrentPath = "/Users/jamesbrown/Downloads/anime_download/[Kamigami&VCB-Studio] Yahari Ore no Seishun Lovecome wa Machigatte Iru. [Ma10p_1080p].torrent"

// require_esm =require('esm')(module)
// const{WebTorrent} = require_esm('webtorrent').default
// console.log('IMPORT PATH?',process.env.NODE_PATH)

// this system sucks. it does not support string concatenation.

import ffmpeg from 'fluent-ffmpeg'

// fuck it. let's symlink the NODE_PATH to here.

import WebTorrent from 'webtorrent'
// // const WebTorrent =await import('webtorrent')
console.log("WEBTORRENT OBJECT?",WebTorrent)
const client = new WebTorrent()

client.add(torrentPath,torrent =>{
    var selectedFiles = torrent.files.find(file =>{
        console.log("FILENAME?", file.name)
        return file.name.endsWith('.mkv')
    })
    console.log("SELECTED FILES?")
    console.log(selectedFiles)
})
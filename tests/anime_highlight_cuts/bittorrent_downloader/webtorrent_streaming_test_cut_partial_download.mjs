
var torrentPath = "/Users/jamesbrown/Downloads/anime_download/[Kamigami&VCB-Studio] Yahari Ore no Seishun Lovecome wa Machigatte Iru. [Ma10p_1080p].torrent"

var selectedFilePath = "[Kamigami&VCB-Studio] Yahari Ore no Seishun Lovecome wa Machigatte Iru. [Ma10p_1080p]/SPs/[Kamigami&VCB-Studio] Yahari Ore no Seishun Lovecome wa Machigatte Iru. [CM01][Ma10p_1080p][x265_flac].mkv"

// require_esm = require('esm')(module)
// const{WebTorrent} = require_esm('webtorrent').default
// console.log('IMPORT PATH?',process.env.NODE_PATH)

// this system sucks. it does not support string concatenation.

// maybe you can execute command to symlink global node_modules automatically? nope in javascript but in shell script, or it will not run as expected, since the import statements are running before anything would. 

import ffmpeg from 'fluent-ffmpeg'

// fuck it. let's symlink the NODE_PATH to here.
// https://github.com/nodejs/node/issues/38687
// https://nodejs.org/api/esm.html#esm_no_node_path
// https://nodejs.org/api/esm.html

// no template string available. shit.

import WebTorrent from 'webtorrent'
// // const WebTorrent = await import('webtorrent')

console.log("WEBTORRENT OBJECT?",WebTorrent)
const client = new WebTorrent()

client.add(torrentPath,torrent =>{
    var selectedFile = torrent.files.find(file =>{
        // console.log("FILENAME?", file.name)
        // it will only select the first file matching the criterion.
        // return file.name.endsWith('.mkv')
        return file.path == selectedFilePath
    })
    // console.log("SELECTED FILE?")
    // console.log(selectedFile)
    // exit here?
    // process.exit()

    // now pass to fluent-ffmpeg.
    const selectedFileStream = selectedFile.
})
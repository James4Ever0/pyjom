
// webtorrent@^1.5.8
// version mismatch?
// nope. check how webtorrent-cli works. your code sucks.

// now: 2.0.1

var torrentPath="/Users/jamesbrown/Downloads/anime_download/[Kamigami&VCB-Studio] Yahari Ore no Seishun Lovecome wa Machigatte Iru. [Ma10p_1080p].torrent"

var selectedFilePath="[Kamigami&VCB-Studio] Yahari Ore no Seishun Lovecome wa Machigatte Iru. [Ma10p_1080p]/SPs/[Kamigami&VCB-Studio] Yahari Ore no Seishun Lovecome wa Machigatte Iru. [CM01][Ma10p_1080p][x265_flac].mkv" // this is goddamn mkv.

// require_esm = require('esm')(module)
// const{WebTorrent} = require_esm('webtorrent').default
// console.log('IMPORT PATH?',process.env.NODE_PATH)

// this system sucks. it does not support string concatenation.

// maybe you can execute command to symlink global node_modules automatically? nope in javascript but in shell script, or it will not run as expected, since the import statements are running before anything would. 

import ffmpeg from 'fluent-ffmpeg'
// import fs from 'fs'

// fuck it. let's symlink the NODE_PATH to here.
// https://github.com/nodejs/node/issues/38687
// https://nodejs.org/api/esm.html#esm_no_node_path
// https://nodejs.org/api/esm.html

// no template string available. shit.

import WebTorrent from 'webtorrent'
// // const WebTorrent = await import('webtorrent')

console.log("WEBTORRENT OBJECT?",WebTorrent)
const client=new WebTorrent({dht: true}) // nothing reading out. guess this is fucked.

const serverPort=8970

const instance=client.createServer()
instance.server.listen(serverPort) // not random port? not zero? 

client.add(torrentPath,torrent => {
    var selectedFile=torrent.files.find(file => {
        // console.log("FILENAME?", file.name)
        // it will only select the first file matching the criterion.
        // return file.name.endsWith('.mkv')
        return file.path==selectedFilePath
    })
    // console.log("SELECTED FILE?")
    // console.log(selectedFile)
    // exit here?
    // process.exit()

    // now pass to fluent-ffmpeg.
    // https://github.com/leeroybrun/webtorrent-transcode

    setInterval(() => {console.log("SPEED?",client.downloadSpeed)},2000)

    // *******************READSTREAM RELATED*******************

    // var stream=selectedFile.createReadStream() // not working! fuck.
    // // var stream = fs.createReadStream("/Users/jamesbrown/Downloads/anime_download/[Sakurato] Onii-chan wa Oshimai! [01][AVC-8bit 1080p AAC][CHT].mp4")
    // stream.unpipe=(nodeStream) => { } //doing nothing?

    // stream.on('error',function(err) {
    //     console.log('STREAM ERROR?',err);
    //     // just ignore it?
    // })

    // console.log("STREAM?",stream)
    // while(true) {
    //     var buffer=stream.read(200)
    //     console.log("READING:",buffer)
    // }
    // var reading=false
    // stream.on('readable',function() {
    //     if(!reading) {
    //         reading=true
    //         console.log("STREAM READABLE")
    //         ffmpeg(stream).ffprobe((err,data) => {
    //             if(err) {
    //                 console.log("FFPROBE ERROR:",err)
    //             } else {
    //                 console.log("FFPROBE METADATA:",data)
    //             }
    //             process.exit()
    //         })
    //     }
    // })

    // duration is fake.


    // ffmpeg(stream).ffprobe((err,data) => {
    //     if(err) {
    //         console.log("FFPROBE ERROR:",err)
    //     } else {
    //         console.log("FFPROBE METADATA:",data)
    //     }
    //     // process.exit()
    // })


    // ffmpeg(stream).seekInput(60).duration(60).on('progress',function(progress) {
    //     console.log('FFmpeg Processing: '+progress.percent+'% done');
    // }).outputOptions('-c copy -y').output('output.mkv').run() // still not working?

    // *******************READSTREAM RELATED*******************

    // how about let's use url?

    // how to urlencode?
    // var urlSuffix = encodeURIComponent(selectedFilePath)

    var fileRequestUrl=`http://localhost:${serverPort}`+selectedFile.streamURL
    console.log("STREAMING URL?",fileRequestUrl)
//shit?

    ffmpeg(fileRequestUrl).ffprobe((err,data) => {
        if(err) {
            console.log("FFPROBE ERROR:",err)
        } else {
            console.log("FFPROBE METADATA:",data)
        }
        // process.exit()
    })

    // ffmpeg(fileRequestUrl).seekInput('3:00').duration().on('progress',function(progress) {
    //     console.log('FFmpeg Processing: '+progress.percent+'% done');
    // }).on('end',() => {

    //     console.log("FFMPEG EXECUTION COMPLETE?")
    //     instance.close()
    //     client.destroy()
    //     process.exit()

    // }).outputOptions(['-c copy','-y']).output('output.mkv').run()


    // not top-level function or async function. fuck.
})
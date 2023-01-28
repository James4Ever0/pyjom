
// webtorrent@^1.5.8
// version mismatch?
// nope. check how webtorrent-cli works. your code sucks.

// now: 2.0.1

// you make countdowns. you use managed temporary directories. you use port within range.

// you might want a single, unified server instance. in that case you will manage resources within server, which could be error prone?

var torrentPath="/Users/jamesbrown/Downloads/anime_download/[Kamigami&VCB-Studio] Yahari Ore no Seishun Lovecome wa Machigatte Iru. [Ma10p_1080p].torrent"

var selectedFilePath="[Kamigami&VCB-Studio] Yahari Ore no Seishun Lovecome wa Machigatte Iru. [Ma10p_1080p]/SPs/[Kamigami&VCB-Studio] Yahari Ore no Seishun Lovecome wa Machigatte Iru. [CM01][Ma10p_1080p][x265_flac].mkv" // this is the goddamnly short mkv.

// var selectedFilePath="[Kamigami&VCB-Studio] Yahari Ore no Seishun Lovecome wa Machigatte Iru. [Ma10p_1080p]/[Kamigami&VCB-Studio] Yahari Ore no Seishun Lovecome wa Machigatte Iru. [OVA][Ma10p_1080p][x265_flac].mkv" // this is long

// require_esm = require('esm')(module)
// const{WebTorrent} = require_esm('webtorrent').default
// console.log('IMPORT PATH?',process.env.NODE_PATH)

// this system sucks. it does not support string concatenation.

// maybe you can execute command to symlink global node_modules automatically? nope in javascript but in shell script, or it will not run as expected, since the import statements are running before anything would. 

import ffmpeg from 'fluent-ffmpeg'
import fs from 'fs'
// try {
fs.rmdirSync('./[Kamigami&VCB-Studio] Yahari Ore no Seishun Lovecome wa Machigatte Iru. [Ma10p_1080p]',{recursive: true})
// maybe we shall not catch this exception? handle it yourself!
// }
// catch(e) { // you can omit the (e)
//     // console.log("GIVEN DIRECTORY DOES NOT EXIST")
//     // it will execute even if the directory does not exist.
//     console.log("UNKNOWN ERROR WHILE REMOVING DIRECTORY:")
//     console.log(e)
// }

// fuck it. let's symlink the NODE_PATH to here.
// https://github.com/nodejs/node/issues/38687
// https://nodejs.org/api/esm.html#esm_no_node_path
// https://nodejs.org/api/esm.html

// no template string available. shit.

// import { Readable } from 'stream'

import WebTorrent from 'webtorrent'
// // const WebTorrent = await import('webtorrent')

console.log("WEBTORRENT OBJECT?",WebTorrent)
const client=new WebTorrent({dht: true}) // nothing reading out. guess this is fucked.
// please cache files under some KNOWN directories. otherwise, i will be fucked.

const serverPort=8970

const instance=client.createServer()
instance.server.listen(serverPort) // not random port? not zero? 

const config={}
// https://github.com/webtorrent/webtorrent/blob/master/docs/api.md#clientaddtorrentid-opts-function-ontorrent-torrent-
config.path=process.cwd() // download to current directory?
// pass different temp directory name for different torrents to prevent name clash? but what about the streaming URL?
// default=`/tmp/webtorrent/`

// now i fucking got you!

// add trackers?
// config.announce=[""]

client.add(torrentPath,config,(torrent) => {
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

    setInterval(() => {console.log("SPEED?",client.downloadSpeed)},2000) // why speed is zero now? wtf? are you finished?

    // *******************READSTREAM RELATED*******************

    // https://github.com/webtorrent/webtorrent/issues/2464
    // const stream = Readable.from(selectedFile) // are you sure?
    // this sucks. pipe is not seekable. consider something else? (like unix domain socket)

    // var stream=selectedFile.createReadStream() // not working! fuck.
    // // // var stream = fs.createReadStream("/Users/jamesbrown/Downloads/anime_download/[Sakurato] Onii-chan wa Oshimai! [01][AVC-8bit 1080p AAC][CHT].mp4")
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


    // ffmpeg(stream).seekInput('0:10').duration("0:15").on('progress',function(progress) {
    //     // why not showing progress?
    //     console.log('FFmpeg Processing: '+progress.percent+'% done');
    // }).on('end',() => {
    //     console.log("FFMPEG EXECUTION COMPLETE?")
    //     // let's rerun.
    //     // instance.close()
    //     client.destroy()
    //     process.exit()
    //     // the time range simply does not exist.
    // }).outputOptions(['-c copy','-y']).output('output.mkv').run() // still not working?

    // *******************READSTREAM RELATED*******************

    // how about let's use url?

    // how to urlencode?
    // var urlSuffix = encodeURIComponent(selectedFilePath)

    var fileRequestUrl=`http://localhost:${serverPort}`+selectedFile.streamURL
    // console.log("STREAMING URL?",fileRequestUrl)

    // http://localhost:8970/webtorrent/421d78cadb5e1bb4fc1fec9dc2d6680e810c13c2/%5BKamigami&VCB-Studio%5D%20Yahari%20Ore%20no%20Seishun%20Lovecome%20wa%20Machigatte%20Iru.%20%5BMa10p_1080p%5D/SPs/%5BKamigami&VCB-Studio%5D%20Yahari%20Ore%20no%20Seishun%20Lovecome%20wa%20Machigatte%20Iru.%20%5BCM01%5D%5BMa10p_1080p%5D%5Bx265_flac%5D.mkv
    //shit?

    // ffmpeg(fileRequestUrl).ffprobe((err,data) => {
    //     if(err) {
    //         console.log("FFPROBE ERROR:",err)
    //     } else {
    //         console.log("FFPROBE METADATA:",data)
    //         var duration=data.format.duration
    //         console.log("VIDEO DURATION?",duration)
    //         // you'd better read this. you fuck!
    //         // i ask for 10 secs.

    //         // output still contains metadata. but do we have subtitles?
    //         // seeking is not so accurate but in minutes? easy.
    //         // for file under 1 minute, please do not seek ok? (seek locally?)
    //         // do not seek for segments that are too short. seek larger segments!

    ffmpeg(fileRequestUrl).seekInput('0:10').duration("0:15").on('progress',function(progress) {
        console.log('FFmpeg Processing: '+progress.percent+'% done');
    }).on('end',() => {
        console.log("FFMPEG EXECUTION COMPLETE?")
        // let's rerun.
        instance.close()
        client.destroy()
        process.exit()
        // the time range simply does not exist.
    }).outputOptions(['-c copy',
        '-y']).output('output.mkv').run()
    // not top-level function or async function. fuck.
})

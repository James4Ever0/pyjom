const FfmpegCommand = (await import(`${process.env.NODE_PATH}/fluent-ffmpeg/index.js`)).default 
const WebTorrent = (await import(`${process.env.NODE_PATH}/webtorrent/index.js`)).default 
// promise!
// shit this ESM can directly use await statements.

console.log(FfmpegCommand)
console.log(typeof(FfmpegCommand)) // "function", with default name.

console.log(WebTorrent)
console.log(typeof(WebTorrent)) // "function"? why i see "class" in console.log?

// this syntax is not recommended. autocompletion will not work.
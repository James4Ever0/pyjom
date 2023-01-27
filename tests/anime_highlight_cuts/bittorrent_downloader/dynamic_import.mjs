const FfmpegCommand = (await import(`${process.env.NODE_PATH}/fluent-ffmpeg/index.js`)).default 
// promise!
// shit this ESM can directly use await statements.

console.log(FfmpegCommand)
console.log(typeof(FfmpegCommand))
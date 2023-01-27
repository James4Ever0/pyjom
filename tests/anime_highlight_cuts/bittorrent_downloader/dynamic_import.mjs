const ffmpeg = (await import(`${process.env.fluent-ffmpeg")).default 
// promise!
// shit this ESM can directly use await statements.

console.log(ffmpeg)
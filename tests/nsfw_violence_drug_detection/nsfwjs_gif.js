const tf = require('@tensorflow/tfjs-node')

const nsfw = require('nsfwjs')


filepath = "/root/Desktop/works/pyjom/samples/video/kitty_flash_15fps_with_mestimate."

// no other classes?
// filepath = "/root/Desktop/works/pyjom/samples/video/cat_invalid_eye_rolling.gif"

const fs = require('fs');

// Store file data chunks in this array
let chunks = [];
// We can use this variable to store the final data
let fileBuffer;

// Read file into stream.Readable
let fileStream = fs.createReadStream(filepath);

// An error occurred with the stream
fileStream.once('error', (err) => {
    // Be sure to handle this properly!
    console.error(err);
});
let _model

const load_model = async() => {
    _model = await nsfw.load()
    console.log('model ready')
}

// Keep the model in memory, make sure it's loaded only once
// File is done being read
fileStream.once('end', () => {
    // create the final data Buffer from data chunks;
    fileBuffer = Buffer.concat(chunks);
    // do shit here.
    console.log("filebuffer ready")
    load_model().then(() => {
        _model.classifyGif(fileBuffer, { topk: 3, fps: 1 })
            .then(predictions => console.log('predictions', predictions))
            .catch(error => console.log('model error', error))
    })

    // Of course, you can do anything else you need to here, like emit an event!
});

// Data is flushed from fileStream in chunks,
// this callback will be executed for each chunk
fileStream.on('data', (chunk) => {
    chunks.push(chunk); // push data chunk to array

    // We can perform actions on the partial data we have so far!
});
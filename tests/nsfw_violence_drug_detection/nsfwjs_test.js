const express = require('express')
const multer = require('multer')
const jpeg = require('jpeg-js')

const tf = require('@tensorflow/tfjs-node')
const nsfw = require('nsfwjs')

const app = express()
const upload = multer()

let _model

// this even works for gif!
// it will normalize and resize the image if needed.
// shall we check for gif?

const convert = async(img) => {
    // Decoded image in UInt8 Byte array
    const image = await jpeg.decode(img, true) //wtf?

    const numChannels = 3
    const numPixels = image.width * image.height
    const values = new Int32Array(numPixels * numChannels)
    // are you sure about the width?

    for (let i = 0; i < numPixels; i++)
        for (let c = 0; c < numChannels; ++c)
            values[i * numChannels + c] = image.data[i * 4 + c]

    return tf.tensor3d(values, [image.height, image.width, numChannels], 'int32')
}

app.post('/nsfw', upload.single('image'), async(req, res) => {
    if (!req.file) res.status(400).send('Missing image multipart/form-data')
    else {
        try {
            const image = await convert(req.file.buffer) // here we have buffer.
            // we need some file format hints.
            const predictions = await _model.classify(image)
            image.dispose()
            res.json(predictions)
        } catch (e) {
            console.log(e)
            res.json({ message: 'error' })
        }

    }
})

const load_model = async() => {
    _model = await nsfw.load()
}

// Keep the model in memory, make sure it's loaded only once
load_model().then(() => app.listen(8511))

// curl --request POST localhost:8080/nsfw --header 'Content-Type: multipart/form-data' --data-binary 'image=@/full/path/to/picture.jpg'
const express = require('express')
const multer = require('multer')
const jpeg = require('jpeg-js')
const bmp = require('bmp-js')
const png = require('png-js')

const tf = require('@tensorflow/tfjs-node')
const nsfw = require('nsfwjs')

const app = express()
const upload = multer()

let _model

// this even works for gif!
// it will normalize and resize the image if needed.
// shall we check for gif?

const convert = async(img, type) => {
    // Decoded image in UInt8 Byte array
    if (type == 'image/jpeg') { const image = await jpeg.decode(img, true) } //wtf?
    // order: rgba
    else if (type == 'image/png') {
        const image = await png.decode(img, true)
    } else if (type == 'image/bmp') {
        const image = await bmp.decode(img, true)
    }

    const numChannels = 3
    const numPixels = image.width * image.height
    const values = new Int32Array(numPixels * numChannels)
        // are you sure about the width?

    for (let i = 0; i < numPixels; i++)
        for (let c = 0; c < numChannels; ++c)
            if (type == 'bmp') {
                // ABGR
                values[i * numChannels + c] = image.data[i * 4 + 3 - c]
            } else {
                values[i * numChannels + c] = image.data[i * 4 + c]
            }

    return tf.tensor3d(values, [image.height, image.width, numChannels], 'int32')
}

app.get('/', async(req, res) => {
    res.send('nsfw nodejs server')
})

app.post('/nsfw', upload.single('image'), async(req, res) => {
    if (!req.file) res.status(400).send('Missing image multipart/form-data')
    else {
        try {
            console.log('file uploaded:', req.file)
            if (req.file.fieldname == 'image') {
                type = req.file.mimetype // deal with it later.
                extension = req.file.originalname.split(".").slice(-1)[0].toLowerCase()
                if (extension == 'gif' || type == 'image/gif') {
                    const image = req.file.buffer
                    const predictions = await _model.classifyGif(image, { topk: 3, fps: 1 })
                    image.dispose()
                    res.json(predictions)
                } else {
                    if (extension == 'bmp') {
                        type = 'image/bmp'
                    }
                    const image = await convert(req.file.buffer, type) // here we have buffer.
                    const predictions = await _model.classify(image)
                    image.dispose()
                    res.json(predictions)
                }
            }
            // we need some file format hints.

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
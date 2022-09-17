import { createRequire } from "module";
const require = createRequire(import.meta.url);

const express = require('express')
const multer = require('multer')
const jpeg = require('jpeg-js')
    // const bmp = require('bmp-js')
const bmp = require('bmp-ts');
// const bmpBuffer = fs.readFileSync('bit24.bmp');
const { PNG } = require('pngjs')

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
    let image
    if (type == 'image/jpeg') {
        image = await jpeg.decode(img, true)
            // RGBA
    } //wtf?
    // order: rgba
    else if (type == 'image/png') {
        image = PNG.sync.read(img)
    } else if (type == 'image/bmp') {
        // image = await bmp.decode(img, true)
        image = bmp.decode(img, { toRGBA: true });

    }

    const numChannels = 3
    const numPixels = image.width * image.height // will raise an error if image is not acquired.
    const values = new Int32Array(numPixels * numChannels)
        // are you sure about the width?

    // can you make this faster? shit?
    // this shit is no numpy. fuck.
    for (let i = 0; i < numPixels; i++)
        for (let c = 0; c < numChannels; ++c)
        // if (type == 'bmp') {
        //     // ABGR?
        //     // values[i * numChannels + c] = image.data[i * 4+c]
        //     values[i * numChannels + c] = image.data[i * 4 + 3 - c]
        // } else {
            values[i * numChannels + c] = image.data[i * 4 + c]
            // }

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
                    let image = req.file.buffer
                    let predictions = await _model.classifyGif(image, { topk: 3, fps: 1 })
                        // image.dispose()
                    predictions.message = 'success'
                    res.json(predictions)
                } else {
                    if (extension == 'bmp') {
                        type = 'image/bmp'
                    }
                    let image = await convert(req.file.buffer, type) // here we have buffer.
                    let predictions = await _model.classify(image)
                    predictions.message = 'success'
                        // image.dispose()
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
load_model().then(() => {
    console.log('server ready')
    app.listen(8511)
})

// curl --request POST localhost:8080/nsfw --header 'Content-Type: multipart/form-data' --data-binary 'image=@/full/path/to/picture.jpg'
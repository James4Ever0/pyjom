// import { createRequire } from "module";
// const require = createRequire(import.meta.url);
function maskColor(maskRed, maskGreen, maskBlue, maskAlpha) {
    const maskRedR = (~maskRed + 1) & maskRed;
    const maskGreenR = (~maskGreen + 1) & maskGreen;
    const maskBlueR = (~maskBlue + 1) & maskBlue;
    const maskAlphaR = (~maskAlpha + 1) & maskAlpha;
    const shiftedMaskRedL = maskRed / maskRedR + 1;
    const shiftedMaskGreenL = maskGreen / maskGreenR + 1;
    const shiftedMaskBlueL = maskBlue / maskBlueR + 1;
    const shiftedMaskAlphaL = maskAlpha / maskAlphaR + 1;
    return {
        shiftRed: (x) => (((x & maskRed) / maskRedR) * 0x100) / shiftedMaskRedL,
        shiftGreen: (x) => (((x & maskGreen) / maskGreenR) * 0x100) / shiftedMaskGreenL,
        shiftBlue: (x) => (((x & maskBlue) / maskBlueR) * 0x100) / shiftedMaskBlueL,
        shiftAlpha: maskAlpha !== 0 ?
            (x) => (((x & maskAlpha) / maskAlphaR) * 0x100) / shiftedMaskAlphaL :
            () => 255
    };
}

var HeaderTypes;
(function(HeaderTypes) {
    HeaderTypes[HeaderTypes["BITMAP_INFO_HEADER"] = 40] = "BITMAP_INFO_HEADER";
    HeaderTypes[HeaderTypes["BITMAP_V2_INFO_HEADER"] = 52] = "BITMAP_V2_INFO_HEADER";
    HeaderTypes[HeaderTypes["BITMAP_V3_INFO_HEADER"] = 56] = "BITMAP_V3_INFO_HEADER";
    HeaderTypes[HeaderTypes["BITMAP_V4_HEADER"] = 108] = "BITMAP_V4_HEADER";
    HeaderTypes[HeaderTypes["BITMAP_V5_HEADER"] = 124] = "BITMAP_V5_HEADER";
})(HeaderTypes || (HeaderTypes = {}));

class BmpDecoder {
    constructor(buffer, { toRGBA } = { toRGBA: false }) {
        this.buffer = buffer;
        this.toRGBA = !!toRGBA;
        this.pos = 0;
        this.bottomUp = true;
        this.flag = this.buffer.toString('utf-8', 0, (this.pos += 2));
        if (this.flag !== 'BM') {
            throw new Error('Invalid BMP File');
        }
        this.locRed = this.toRGBA ? 0 : 3;
        this.locGreen = this.toRGBA ? 1 : 2;
        this.locBlue = this.toRGBA ? 2 : 1;
        this.locAlpha = this.toRGBA ? 3 : 0;
        this.parseHeader();
        this.parseRGBA();
    }
    parseHeader() {
        this.fileSize = this.readUInt32LE();
        this.reserved1 = this.buffer.readUInt16LE(this.pos);
        this.pos += 2;
        this.reserved2 = this.buffer.readUInt16LE(this.pos);
        this.pos += 2;
        this.offset = this.readUInt32LE();
        // End of BITMAP_FILE_HEADER
        this.headerSize = this.readUInt32LE();
        if (!(this.headerSize in HeaderTypes)) {
            throw new Error(`Unsupported BMP header size ${this.headerSize}`);
        }
        this.width = this.readUInt32LE();
        this.height = this.readUInt32LE();
        this.planes = this.buffer.readUInt16LE(this.pos);
        this.pos += 2;
        this.bitPP = this.buffer.readUInt16LE(this.pos);
        this.pos += 2;
        this.compression = this.readUInt32LE();
        this.rawSize = this.readUInt32LE();
        this.hr = this.readUInt32LE();
        this.vr = this.readUInt32LE();
        this.colors = this.readUInt32LE();
        this.importantColors = this.readUInt32LE();
        // De facto defaults
        if (this.bitPP === 32) {
            this.maskAlpha = 0;
            this.maskRed = 0x00ff0000;
            this.maskGreen = 0x0000ff00;
            this.maskBlue = 0x000000ff;
        } else if (this.bitPP === 16) {
            this.maskAlpha = 0;
            this.maskRed = 0x7c00;
            this.maskGreen = 0x03e0;
            this.maskBlue = 0x001f;
        }
        // End of BITMAP_INFO_HEADER
        if (this.headerSize > HeaderTypes.BITMAP_INFO_HEADER ||
            this.compression === 3 /* BI_BIT_FIELDS */ ||
            this.compression === 6 /* BI_ALPHA_BIT_FIELDS */ ) {
            this.maskRed = this.readUInt32LE();
            this.maskGreen = this.readUInt32LE();
            this.maskBlue = this.readUInt32LE();
        }
        // End of BITMAP_V2_INFO_HEADER
        if (this.headerSize > HeaderTypes.BITMAP_V2_INFO_HEADER ||
            this.compression === 6 /* BI_ALPHA_BIT_FIELDS */ ) {
            this.maskAlpha = this.readUInt32LE();
        }
        // End of BITMAP_V3_INFO_HEADER
        if (this.headerSize > HeaderTypes.BITMAP_V3_INFO_HEADER) {
            this.pos +=
                HeaderTypes.BITMAP_V4_HEADER - HeaderTypes.BITMAP_V3_INFO_HEADER;
        }
        // End of BITMAP_V4_HEADER
        if (this.headerSize > HeaderTypes.BITMAP_V4_HEADER) {
            this.pos += HeaderTypes.BITMAP_V5_HEADER - HeaderTypes.BITMAP_V4_HEADER;
        }
        // End of BITMAP_V5_HEADER
        if (this.bitPP <= 8 || this.colors > 0) {
            const len = this.colors === 0 ? 1 << this.bitPP : this.colors;
            this.palette = new Array(len);
            for (let i = 0; i < len; i++) {
                const blue = this.buffer.readUInt8(this.pos++);
                const green = this.buffer.readUInt8(this.pos++);
                const red = this.buffer.readUInt8(this.pos++);
                const quad = this.buffer.readUInt8(this.pos++);
                this.palette[i] = {
                    red,
                    green,
                    blue,
                    quad
                };
            }
        }
        // End of color table
        // Can the height ever be negative?
        if (this.height < 0) {
            this.height *= -1;
            this.bottomUp = false;
        }
        const coloShift = maskColor(this.maskRed, this.maskGreen, this.maskBlue, this.maskAlpha);
        this.shiftRed = coloShift.shiftRed;
        this.shiftGreen = coloShift.shiftGreen;
        this.shiftBlue = coloShift.shiftBlue;
        this.shiftAlpha = coloShift.shiftAlpha;
    }
    parseRGBA() {
        this.data = Buffer.alloc(this.width * this.height * 4);
        switch (this.bitPP) {
            case 1:
                this.bit1();
                break;
            case 4:
                this.bit4();
                break;
            case 8:
                this.bit8();
                break;
            case 16:
                this.bit16();
                break;
            case 24:
                this.bit24();
                break;
            default:
                this.bit32();
        }
    }
    bit1() {
        const xLen = Math.ceil(this.width / 8);
        const mode = xLen % 4;
        const padding = mode !== 0 ? 4 - mode : 0;
        let lastLine;
        this.scanImage(padding, xLen, (x, line) => {
            if (line !== lastLine) {
                lastLine = line;
            }
            const b = this.buffer.readUInt8(this.pos++);
            const location = line * this.width * 4 + x * 8 * 4;
            for (let i = 0; i < 8; i++) {
                if (x * 8 + i < this.width) {
                    const rgb = this.palette[(b >> (7 - i)) & 0x1];
                    this.data[location + i * this.locAlpha] = 0;
                    this.data[location + i * 4 + this.locBlue] = rgb.blue;
                    this.data[location + i * 4 + this.locGreen] = rgb.green;
                    this.data[location + i * 4 + this.locRed] = rgb.red;
                } else {
                    break;
                }
            }
        });
    }
    bit4() {
        if (this.compression === 2 /* BI_RLE4 */ ) {
            this.data.fill(0);
            let lowNibble = false; //for all count of pixel
            let lines = this.bottomUp ? this.height - 1 : 0;
            let location = 0;
            while (location < this.data.length) {
                const a = this.buffer.readUInt8(this.pos++);
                const b = this.buffer.readUInt8(this.pos++);
                //absolute mode
                if (a === 0) {
                    if (b === 0) {
                        //line end
                        lines += this.bottomUp ? -1 : 1;
                        location = lines * this.width * 4;
                        lowNibble = false;
                        continue;
                    }
                    if (b === 1) {
                        // image end
                        break;
                    }
                    if (b === 2) {
                        // offset x, y
                        const x = this.buffer.readUInt8(this.pos++);
                        const y = this.buffer.readUInt8(this.pos++);
                        lines += this.bottomUp ? -y : y;
                        location += y * this.width * 4 + x * 4;
                    } else {
                        let c = this.buffer.readUInt8(this.pos++);
                        for (let i = 0; i < b; i++) {
                            location = this.setPixelData(location, lowNibble ? c & 0x0f : (c & 0xf0) >> 4);
                            if (i & 1 && i + 1 < b) {
                                c = this.buffer.readUInt8(this.pos++);
                            }
                            lowNibble = !lowNibble;
                        }
                        if ((((b + 1) >> 1) & 1) === 1) {
                            this.pos++;
                        }
                    }
                } else {
                    //encoded mode
                    for (let i = 0; i < a; i++) {
                        location = this.setPixelData(location, lowNibble ? b & 0x0f : (b & 0xf0) >> 4);
                        lowNibble = !lowNibble;
                    }
                }
            }
        } else {
            const xLen = Math.ceil(this.width / 2);
            const mode = xLen % 4;
            const padding = mode !== 0 ? 4 - mode : 0;
            this.scanImage(padding, xLen, (x, line) => {
                const b = this.buffer.readUInt8(this.pos++);
                const location = line * this.width * 4 + x * 2 * 4;
                const first4 = b >> 4;
                let rgb = this.palette[first4];
                this.data[location] = 0;
                this.data[location + 1] = rgb.blue;
                this.data[location + 2] = rgb.green;
                this.data[location + 3] = rgb.red;
                if (x * 2 + 1 >= this.width) {
                    // throw new Error('Something');
                    return false;
                }
                const last4 = b & 0x0f;
                rgb = this.palette[last4];
                this.data[location + 4] = 0;
                this.data[location + 4 + 1] = rgb.blue;
                this.data[location + 4 + 2] = rgb.green;
                this.data[location + 4 + 3] = rgb.red;
            });
        }
    }
    bit8() {
        if (this.compression === 1 /* BI_RLE8 */ ) {
            this.data.fill(0);
            let lines = this.bottomUp ? this.height - 1 : 0;
            let location = 0;
            while (location < this.data.length) {
                const a = this.buffer.readUInt8(this.pos++);
                const b = this.buffer.readUInt8(this.pos++);
                //absolute mode
                if (a === 0) {
                    if (b === 0) {
                        //line end
                        lines += this.bottomUp ? -1 : 1;
                        location = lines * this.width * 4;
                        continue;
                    }
                    if (b === 1) {
                        //image end
                        break;
                    }
                    if (b === 2) {
                        //offset x,y
                        const x = this.buffer.readUInt8(this.pos++);
                        const y = this.buffer.readUInt8(this.pos++);
                        lines += this.bottomUp ? -y : y;
                        location += y * this.width * 4 + x * 4;
                    } else {
                        for (let i = 0; i < b; i++) {
                            const c = this.buffer.readUInt8(this.pos++);
                            location = this.setPixelData(location, c);
                        }
                        // @ts-ignore
                        const shouldIncrement = b & (1 === 1);
                        if (shouldIncrement) {
                            this.pos++;
                        }
                    }
                } else {
                    //encoded mode
                    for (let i = 0; i < a; i++) {
                        location = this.setPixelData(location, b);
                    }
                }
            }
        } else {
            const mode = this.width % 4;
            const padding = mode !== 0 ? 4 - mode : 0;
            this.scanImage(padding, this.width, (x, line) => {
                const b = this.buffer.readUInt8(this.pos++);
                const location = line * this.width * 4 + x * 4;
                if (b < this.palette.length) {
                    const rgb = this.palette[b];
                    this.data[location] = 0;
                    this.data[location + 1] = rgb.blue;
                    this.data[location + 2] = rgb.green;
                    this.data[location + 3] = rgb.red;
                } else {
                    this.data[location] = 0;
                    this.data[location + 1] = 0xff;
                    this.data[location + 2] = 0xff;
                    this.data[location + 3] = 0xff;
                }
            });
        }
    }
    bit16() {
        const padding = (this.width % 2) * 2;
        this.scanImage(padding, this.width, (x, line) => {
            const loc = line * this.width * 4 + x * 4;
            const px = this.buffer.readUInt16LE(this.pos);
            this.pos += 2;
            this.data[loc + this.locRed] = this.shiftRed(px);
            this.data[loc + this.locGreen] = this.shiftGreen(px);
            this.data[loc + this.locBlue] = this.shiftBlue(px);
            this.data[loc + this.locAlpha] = this.shiftAlpha(px);
        });
    }
    bit24() {
        const padding = this.width % 4;
        this.scanImage(padding, this.width, (x, line) => {
            const loc = line * this.width * 4 + x * 4;
            const blue = this.buffer.readUInt8(this.pos++);
            const green = this.buffer.readUInt8(this.pos++);
            const red = this.buffer.readUInt8(this.pos++);
            this.data[loc + this.locRed] = red;
            this.data[loc + this.locGreen] = green;
            this.data[loc + this.locBlue] = blue;
            this.data[loc + this.locAlpha] = 0;
        });
    }
    bit32() {
        this.scanImage(0, this.width, (x, line) => {
            const loc = line * this.width * 4 + x * 4;
            const px = this.readUInt32LE();
            this.data[loc + this.locRed] = this.shiftRed(px);
            this.data[loc + this.locGreen] = this.shiftGreen(px);
            this.data[loc + this.locBlue] = this.shiftBlue(px);
            this.data[loc + this.locAlpha] = this.shiftAlpha(px);
        });
    }
    scanImage(padding = 0, width = this.width, processPixel) {
        for (let y = this.height - 1; y >= 0; y--) {
            const line = this.bottomUp ? y : this.height - 1 - y;
            for (let x = 0; x < width; x++) {
                const result = processPixel.call(this, x, line);
                if (result === false) {
                    return;
                }
            }
            this.pos += padding;
        }
    }
    readUInt32LE() {
        const value = this.buffer.readUInt32LE(this.pos);
        this.pos += 4;
        return value;
    }
    setPixelData(location, rgbIndex) {
        const { blue, green, red } = this.palette[rgbIndex];
        this.data[location + this.locAlpha] = 0;
        this.data[location + 1 + this.locBlue] = blue;
        this.data[location + 2 + this.locGreen] = green;
        this.data[location + 3 + this.locRed] = red;
        return location + 4;
    }
}

const express = require('express')
const multer = require('multer')
const jpeg = require('jpeg-js')
    // const bmp = require('bmp-js')
    // const bmp = require('bmp-ts').default;
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
        image = new BmpDecoder(img, { toRGBA: true });

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
const fs = require('fs')
const {promisify} = require('util')
const readFileAsync = promisify(fs.readFile)
const {equal} = require('assert')
const shiftjis = require('../lib')

describe('shiftjis', () => {
  it('decode', async () => {
    const data = await readFileAsync('misc/shift_jis.txt')
    const str = shiftjis.decode(data)
    equal(str.trim(), 'これはペンです。\nThis is a pen.')
  })

  it('encode', async () => {
    const str = 'これはペンです。'
    const encoded = shiftjis.encode(str)
    const decoded = shiftjis.decode(encoded)
    equal(decoded, str)
  })
})

/* global describe it */

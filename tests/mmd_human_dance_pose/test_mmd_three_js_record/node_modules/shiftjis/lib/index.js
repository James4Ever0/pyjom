const iconv = require('iconv-lite')
const SHIFT_JIS = 'Shift_JIS'

module.exports = {
  decode (data) {
    const str = iconv.decode(data, SHIFT_JIS)
    return str
  },
  encode (str) {
    const buf = iconv.encode(str, SHIFT_JIS)
    return buf
  }
}

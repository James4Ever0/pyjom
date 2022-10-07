/* globals __line */

const path = require('path')
const createContext = require('../../index')
const utils = require('../common/utils.js')
const utilsLog = require('../common/utils_log.js')
const log = new utilsLog.Log(path.basename(__filename), 'DEBUG')

function main () {
  // Create context
  const width = 512
  const height = 512
  const gl = createContext(width, height)

  // Clear screen to red
  gl.clearColor(1.0, 0.0, 0.0, 1.0)
  gl.colorMask(true, true, true, true)
  gl.clear(gl.COLOR_BUFFER_BIT)

  var filename = __filename + '.ppm' // eslint-disable-line
  log.info(__line, 'rendering ' + filename)
  utils.bufferToFile(gl, width, height, filename)
  log.info(__line, 'finished rendering ' + filename)

  gl.destroy()
}

main()

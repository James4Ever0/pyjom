const createContext = require('../index')
const utils = require('./utils.js')

function main () {
  // Create context
  const width = 64
  const height = 64
  const gl = createContext(width, height)

  // Clear screen to red
  gl.clearColor(1.0, 0.0, 0.0, 1.0)
  gl.colorMask(true, true, true, true)
  gl.clear(gl.COLOR_BUFFER_BIT)

  utils.dumpBuffer(gl, width, height)

  gl.destroy()
}

main()

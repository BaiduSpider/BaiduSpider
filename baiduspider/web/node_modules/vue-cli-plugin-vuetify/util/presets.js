const fs = require('fs')
const path = require('path')
const resolve = file => path.resolve(__dirname, file)

const PRESET_MAP = {
  default: 'Default (recommended)',
  prototype: 'Prototype (rapid development)',
}

module.exports = fs.readdirSync(resolve('../presets')).map(preset => {
  const value = preset.split('.').shift()

  return { name: PRESET_MAP[value], value }
})

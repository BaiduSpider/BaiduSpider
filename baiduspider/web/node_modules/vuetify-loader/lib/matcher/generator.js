const Module = require('module')
const originalLoader = Module._load
const { readdirSync, statSync } = require('fs')
const { dirname, join } = require('path')

Module._load = function _load (request, parent) {
  if (request.endsWith('.styl')) return
  if (request.endsWith('.scss')) return
  if (request.endsWith('.sass')) return
  else return originalLoader(request, parent)
}

const directives = Object.keys(require('vuetify/es5/directives'))
  .filter(val => val !== 'default')

const dir = dirname(require.resolve('vuetify/es5/components'))

const components = new Map()
readdirSync(dir).forEach(group => {
  if (!statSync(join(dir, group)).isDirectory()) return

  const component = require(`vuetify/es5/components/${group}`).default
  if (component.hasOwnProperty('$_vuetify_subcomponents')) {
    Object.keys(component.$_vuetify_subcomponents)
      .forEach(name => components.set(name, group))
  } else {
    components.set(group, group)
  }
})

Module._load = originalLoader

module.exports = {
  directives,
  components
}

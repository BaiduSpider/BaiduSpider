// Imports
const fs = require('fs')
const helpers = require('./helpers')

function addDependencies (api) {
  api.extendPackage({
    dependencies: {
      vuetify: '^2.2.11',
    },
  })
}

function renderFiles (api, { opts }) {
  const ext = api.hasPlugin('typescript') ? 'ts' : 'js'
  const pluginFilename = `vuetify.${ext}`

  api.render({
    [`./src/plugins/${pluginFilename}`]: '../templates/default/src/plugins/vuetify.js',
  }, {
    ...opts,
    typescript: api.hasPlugin('typescript'),
  })

  // Render files if we're replacing
  const fs = require('fs')
  const routerPath = api.resolve(`./src/router.${ext}`)
  opts.router = fs.existsSync(routerPath)

  if (opts.replaceComponents) {
    const files = {
      './src/App.vue': `../templates/default/src/App.${ext}.vue`,
      './src/assets/logo.svg': '../templates/default/src/assets/logo.svg',
      './src/components/HelloWorld.vue': `../templates/default/src/components/HelloWorld.${ext}.vue`,
    }

    if (opts.router) {
      files['./src/views/Home.vue'] = `../templates/default/src/views/Home.${ext}.vue`
    }

    api.render(files, opts)
  }
}

function addImports (api) {
  api.injectImports(api.entryFile, 'import vuetify from \'./plugins/vuetify\';')
  api.injectRootOptions(api.entryFile, 'vuetify')
}

function setHtmlLang (api, locale) {
  helpers.updateFile(api, './public/index.html', lines => {
    const htmlIndex = lines.findIndex(line => line.match(/<html\s+(.+\s+)?lang=[^\s>]+(\s|>)/))

    if (htmlIndex !== -1) {
      lines[htmlIndex] = lines[htmlIndex].replace(/(<html\s+(.+\s+)?)(lang=)([^\s>]+)(\s|>)/, `$1$3"${locale}"$5`)
    }

    return lines
  })
}

function updateOrCreateVueConfig (api) {
  const config = api.resolve('vue.config.js')

  if (!fs.existsSync(config)) {
    fs.writeFileSync(config, 'module.exports = {}', 'utf8')
  }

  const file = require(config)

  if (!file.transpileDependencies) {
    file.transpileDependencies = []
  }

  if (!file.transpileDependencies.includes('vuetify')) {
    file.transpileDependencies.push('vuetify')
  }

  fs.writeFileSync(config, `module.exports = ${JSON.stringify(file, 2, 2)}`, 'utf8')
}

module.exports = {
  addDependencies,
  addImports,
  renderFiles,
  setHtmlLang,
  updateOrCreateVueConfig,
}

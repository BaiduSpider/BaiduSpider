const helpers = require('./helpers')
const fs = require('fs')

function addDependencies (api) {
  api.extendPackage({
    dependencies: {
      '@babel/polyfill': '^7.4.4',
    },
  })
}

function updateBabelConfig (api) {
  helpers.updateBabelConfig(api, cfg => {
    if (!cfg.presets) return cfg

    const vuePresetIndex = cfg.presets.findIndex(p => Array.isArray(p) ? p[0] === '@vue/app' : p === '@vue/app')
    const isArray = Array.isArray(cfg.presets[vuePresetIndex])

    if (vuePresetIndex < 0) return cfg

    if (isArray) {
      cfg.presets[vuePresetIndex][1].useBuiltIns = 'entry'
    } else {
      cfg.presets[vuePresetIndex] = [
        '@vue/app',
        {
          useBuiltIns: 'entry',
        },
      ]
    }

    return cfg
  })
}

function updateBrowsersList (api) {
  const pkgPath = api.resolve('./package.json')
  const pkg = JSON.parse(fs.readFileSync(pkgPath, { encoding: 'utf8' }))
  const isInPackage = !!pkg.browserslist

  const findIeIndex = lines => lines.findIndex(line => line.match(/^([^\s]*\s+|)ie\s*</))

  if (isInPackage) {
    const ieLineIndex = findIeIndex(pkg.browserslist)

    if (ieLineIndex === -1) {
      pkg.browserslist.push('not ie <= 10')
    } else {
      pkg.browserslist[ieLineIndex] = 'not ie <= 10'
    }

    fs.writeFileSync(
      pkgPath,
      JSON.stringify(pkg, null, 2),
      { encoding: 'utf8' },
    )
  } else {
    helpers.updateFile(api, './.browserslistrc', lines => {
      if (!lines.length) {
        return [
          '> 1%',
          'last 2 versions',
          'not ie <= 10',
        ]
      }

      const ieLineIndex = findIeIndex(lines)
      if (ieLineIndex === -1) {
        lines.push('not ie <= 10')
      } else {
        lines[ieLineIndex] = 'not ie <= 10'
      }

      return lines
    })
  }
}

function addImports (api) {
  api.injectImports(api.entryFile, 'import \'@babel/polyfill\'')
}

module.exports = {
  addDependencies,
  updateBabelConfig,
  addImports,
  updateBrowsersList,
}

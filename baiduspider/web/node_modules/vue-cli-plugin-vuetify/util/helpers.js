// Imports
const semver = require('semver')
const fs = require('fs')

// Check for existence of file and add import
function addImport (api, file, data, folder, end) {
  // sass & scss file types
  for (const ext of ['sass', 'scss']) {
    const path = `${folder}/${file}.${ext}`

    // If file doesn't exist in user
    // project, continue to next
    if (!fileExists(api, `src/${path}`)) continue

    // If file exists, push it into
    // the import statement
    data.push(`@import '@/${path}${end}`)
  }
}

// Go through each folder and add available imports
function addImports (api, file, data, end) {
  // supported folders that can contain
  // a variables or lists file
  for (const folder of ['sass', 'scss', 'styles']) {
    addImport(api, file, data, folder, end)
  }
}

// Check if file exists in user project
function fileExists (api, file) {
  return fs.existsSync(api.resolve(file))
}

// Create an import statement
// to bootstrap a users variables
function mergeRules (api, opt, ext) {
  const data = []
  const end = ext === 'sass' ? "'" : "';"

  addImports(api, 'variables', data, end)

  // If user isn't supplying variables, avoid prepending data
  if (!data.length) return opt

  // Inject Vuetify styles at the end of user supplied
  data.push(`@import '~vuetify/src/styles/styles.sass${end}`)

  let sassLoaderVersion
  try {
    sassLoaderVersion = semver.major(require('sass-loader/package.json').version)
  } catch (e) {}

  // Merge with user-defined loader data config
  if (sassLoaderVersion < 8) {
    if (opt.data) data.unshift(opt.data)

    opt.data = data.join('\n')
  } else {
    if (opt.prependData) data.unshift(opt.prependData)

    opt.prependData = data.join('\n')
  }

  return opt
}

module.exports = {
  addImport,
  addImports,
  fileExists,
  mergeRules,
}

const path = require('path')
const loaderUtils = require('loader-utils')
const compiler = require('vue-template-compiler')

const vuetifyMatcher = require('./matcher/tag')
const vuetifyAttrsMatcher = require('./matcher/attr')
const { camelize, capitalize, hyphenate, requirePeer } = require('./util')
const runtimePaths = {
  installComponents: require.resolve('./runtime/installComponents'),
  installDirectives: require.resolve('./runtime/installDirectives')
}

function getMatches (type, items, matches, component) {
  const imports = []

  items.forEach(item => {
    for (const matcher of matches) {
      const match = matcher(item, {
        [`kebab${type}`]: hyphenate(item),
        [`camel${type}`]: capitalize(camelize(item)),
        path: this.resourcePath.substring(this.rootContext.length + 1),
        component
      })
      if (match) {
        imports.push(match)
        break
      }
    }
  })

  imports.sort((a, b) => a[0] < b[0] ? -1 : (a[0] > b[0] ? 1 : 0))
  return imports
}

function install (install, content, imports) {
  if (imports.length) {
    let newContent = '/* vuetify-loader */\n'
    newContent += `import ${install} from ${loaderUtils.stringifyRequest(this, '!' + runtimePaths[install])}\n`
    newContent += imports.map(i => i[1]).join('\n') + '\n'
    newContent += `${install}(component, {${imports.map(i => i[0]).join(',')}})\n`

    // Insert our modification before the HMR code
    const hotReload = content.indexOf('/* hot reload */')
    if (hotReload > -1) {
      content = content.slice(0, hotReload) + newContent + '\n\n' + content.slice(hotReload)
    } else {
      content += '\n\n' + newContent
    }
  }

  return content
}

module.exports = async function (content, sourceMap) {
  this.async()
  this.cacheable()

  const options = {
    match: [],
    attrsMatch: [],
    ...loaderUtils.getOptions(this)
  }

  if (!Array.isArray(options.match)) options.match = [options.match]
  if (!Array.isArray(options.attrsMatch)) options.attrsMatch = [options.attrsMatch]

  options.match.push(vuetifyMatcher)
  options.attrsMatch.push(vuetifyAttrsMatcher)

  if (!this.resourceQuery) {
    const readFile = path => new Promise((resolve, reject) => {
      this.fs.readFile(path, function (err, data) {
        if (err) reject(err)
        else resolve(data)
      })
    })

    this.addDependency(this.resourcePath)

    const tags = new Set()
    const attrs = new Set()
    const file = (await readFile(this.resourcePath)).toString('utf8')
    const component = compiler.parseComponent(file)
    if (component.template) {
      if (component.template.src) {
        const externalFile = (await new Promise((resolve, reject) =>
          this.resolve(path.dirname(this.resourcePath), component.template.src, (err, result) => {
            if (err) reject(err)
            else resolve(result)
          })
        ))
        const externalContent = (await readFile(externalFile)).toString('utf8')
        component.template.content = externalContent
      }
      if (component.template.lang === 'pug') {
        const pug = requirePeer('pug')
        try {
          component.template.content = pug.render(component.template.content, {filename: this.resourcePath})
        } catch (err) {/* Ignore compilation errors, they'll be picked up by other loaders */}
      }
      compiler.compile(component.template.content, {
        modules: [{
          postTransformNode: node => {
            if ("directives" in node) {
              node.directives.forEach(({ name }) => attrs.add(name))
            }
            tags.add(node.tag)
          }
        }]
      })
    }

    content = install.call(this, 'installComponents', content, getMatches.call(this, 'Tag', tags, options.match, component))
    content = install.call(this, 'installDirectives', content, getMatches.call(this, 'Attr', attrs, options.attrsMatch, component))
  }

  this.callback(null, content, sourceMap)
}

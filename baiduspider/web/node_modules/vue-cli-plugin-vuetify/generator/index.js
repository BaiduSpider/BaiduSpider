module.exports = (api, opts) => {
  const alaCarte = require('./tools/alaCarte')
  const fonts = require('./tools/fonts')
  const polyfill = require('./tools/polyfill')
  const vuetify = require('./tools/vuetify')

  if (opts.preset !== 'configure') {
    opts = require(`../presets/${opts.preset}`).plugins['vue-cli-plugin-vuetify']
  }

  // Add imports
  // Must be before dependencies because of weird bug
  vuetify.addImports(api)
  if (!opts.useAlaCarte && opts.usePolyfill) polyfill.addImports(api)
  if (opts.installFonts) fonts.addImports(api, opts.iconFont)

  // Add dependencies
  vuetify.addDependencies(api)
  if (opts.useAlaCarte) alaCarte.addDependencies(api)
  else if (opts.usePolyfill) polyfill.addDependencies(api)

  if (opts.installFonts) fonts.addDependencies(api, opts.iconFont)

  // Update templates
  vuetify.renderFiles(api, { opts })

  // adapted from https://github.com/Akryum/vue-cli-plugin-apollo/blob/master/generator/index.js#L68-L91
  api.onCreateComplete(() => {
    if (!opts.useAlaCarte && opts.usePolyfill) {
      polyfill.updateBabelConfig(api)
      polyfill.updateBrowsersList(api)
    }
    if (!opts.installFonts) fonts.addLinks(api, opts.iconFont)
    vuetify.setHtmlLang(api, opts.locale)

    // Update vue.config.js for transpileDependency if AlaCarte
    if (opts.useAlaCarte) vuetify.updateOrCreateVueConfig(api)

    api.exitLog('Discord community: https://community.vuetifyjs.com')
    api.exitLog('Github: https://github.com/vuetifyjs/vuetify')
    api.exitLog('Support Vuetify: https://github.com/sponsors/johnleider')
  })
}

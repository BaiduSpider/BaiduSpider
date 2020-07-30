const RuleSet = require('webpack/lib/RuleSet')
const progressiveLoaderModule = require('../progressive-loader/module')
let vueLoaderPath
try {
  vueLoaderPath = require.resolve('vue-loader')
} catch (err) {}

function isVueLoader (use) {
  return use.ident === 'vue-loader-options' ||
    use.loader === 'vue-loader' ||
    (vueLoaderPath && use.loader === vueLoaderPath)
}

class VuetifyLoaderPlugin {
  constructor (options) {
    this.options = options || {}
  }

  apply (compiler) {
    // use webpack's RuleSet utility to normalize user rules
    const rawRules = compiler.options.module.rules
    const { rules } = new RuleSet(rawRules)
    this.rules = rules

    // find the rules that apply to vue files
    const vueRules = rules.filter(rule => rule.use && rule.use.find(isVueLoader))

    if (!vueRules.length) {
      throw new Error(
        `[VuetifyLoaderPlugin Error] No matching rule for vue-loader found.\n` +
        `Make sure there is at least one root-level rule that uses vue-loader.`
      )
    }

    vueRules.forEach(this.updateRule.bind(this))

    compiler.options.module.rules = rules
  }

  updateRule (rule) {
    if (this.options.progressiveImages) {
      const vueLoaderOptions = rule.use.find(isVueLoader).options
      vueLoaderOptions.compilerOptions = vueLoaderOptions.compilerOptions || {}
      vueLoaderOptions.compilerOptions.modules = vueLoaderOptions.compilerOptions.modules || []
      vueLoaderOptions.compilerOptions.modules.push(progressiveLoaderModule)

      const imageRuleIndex = this.rules.findIndex(rule => {
        return rule.resource &&
          !rule.resourceQuery &&
          ['.png', '.jpg', '.jpeg', '.gif'].some(ext => rule.resource(ext))
      })
      let imageRule = this.rules[imageRuleIndex]

      const options = typeof this.options.progressiveImages === 'boolean'
        ? undefined
        : this.options.progressiveImages

      if (!imageRule) {
        imageRule = {
          test: /\.(png|jpe?g|gif|svg|eot|ttf|woff|woff2)(\?.*)?$/,
          oneOf: [
            {
              test: /\.(png|jpe?g|gif)$/,
              resourceQuery: options ? options.resourceQuery : /vuetify-preload/,
              use: [
                {
                  loader: 'vuetify-loader/progressive-loader',
                  options
                },
                {
                  loader: 'url-loader',
                  options: { limit: 8000 }
                }
              ]
            },
            {
              loader: 'url-loader',
              options: { limit: 8000 }
            }
          ]
        }
        rules.push(imageRule)
      } else {
        if (Array.isArray(imageRule.use)) {
          imageRule.oneOf = [
            {
              test: /\.(png|jpe?g|gif)$/,
              resourceQuery: options ? options.resourceQuery : /vuetify-preload/,
              use: [
                {
                  loader: 'vuetify-loader/progressive-loader',
                  options
                },
                ...imageRule.use
              ]
            },
            ...imageRule.use
          ]
        } else if (imageRule.loader) {
          imageRule.oneOf = [
            {
              test: /\.(png|jpe?g|gif)$/,
              resourceQuery: options ? options.resourceQuery : /vuetify-preload/,
              use: [
                {
                  loader: 'vuetify-loader/progressive-loader',
                  options
                },
                {
                  loader: imageRule.loader,
                  options: imageRule.options
                }
              ]
            },
            {
              loader: imageRule.loader,
              options: imageRule.options
            }
          ]
        }
        delete imageRule.use
        delete imageRule.loader
        delete imageRule.options
      }
    }

    rule.oneOf = [
      {
        resourceQuery: '?',
        use: rule.use
      },
      {
        use: [
          {
            loader: require.resolve('./loader'),
            options: {
              match: this.options.match || [],
              attrsMatch: this.options.attrsMatch || []
            }
          },
          ...rule.use
        ]
      },
    ]
    delete rule.use
  }
}

module.exports = VuetifyLoaderPlugin

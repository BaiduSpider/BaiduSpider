const { components } = require('./generator')

module.exports = function match (_, { kebabTag, camelTag: tag }) {
  if (!kebabTag.startsWith('v-')) return

  if (components.has(tag)) {
    return [tag, `import { ${tag} } from 'vuetify/lib/components/${components.get(tag)}';`]
  }
}

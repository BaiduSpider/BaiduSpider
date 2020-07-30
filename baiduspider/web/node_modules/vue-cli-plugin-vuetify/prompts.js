const path = require('path')
const resolve = file => path.resolve(__dirname, file)

const iconfonts = require(resolve('./util/iconfonts.js'))
const presets = require(resolve('./util/presets.js'))
const locales = require(resolve('./util/locales.js'))

function isCustom (answers) {
  return answers.preset === 'configure'
}

module.exports = [
  {
    name: 'preset',
    message: 'Choose a preset:',
    type: 'list',
    choices: [
      ...presets,
      { name: 'Configure (advanced)', value: 'configure' },
    ],
    default: 'default',
  },
  {
    name: 'replaceComponents',
    type: 'confirm',
    message: 'Use a pre-made template? (will replace App.vue and HelloWorld.vue)',
    default: true,
    when: isCustom,
  },
  {
    name: 'useTheme',
    type: 'confirm',
    message: 'Use custom theme?',
    default: false,
    when: isCustom,
  },
  {
    name: 'useCustomProperties',
    type: 'confirm',
    message: 'Use custom properties (CSS variables)?',
    default: false,
    when: isCustom,
  },
  {
    name: 'iconFont',
    type: 'list',
    message: 'Select icon font',
    choices: iconfonts,
    default: 'mdi',
    when: isCustom,
  },
  {
    name: 'installFonts',
    type: 'confirm',
    message: 'Use fonts as a dependency (for Electron or offline)?',
    default: false,
    when: isCustom,
  },
  {
    name: 'useAlaCarte',
    type: 'confirm',
    message: 'Use a-la-carte components?',
    default: true,
    when: isCustom,
  },
  {
    name: 'usePolyfill',
    type: 'confirm',
    message: 'Use babel/polyfill?',
    default: true,
    when: answers => {
      return isCustom(answers) && !answers.useAlaCarte
    },
  },
  {
    name: 'locale',
    type: 'list',
    message: 'Select locale',
    choices: locales,
    default: 'en',
    when: isCustom,
  },
]

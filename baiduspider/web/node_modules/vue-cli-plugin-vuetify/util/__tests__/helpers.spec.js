const helpers = require('../helpers')
const fs = require('fs')

jest.mock('fs')

describe('helpers.js', () => {
  const api = {
    resolve: val => val,
  }

  afterEach(() => {
    fs.existsSync.mockReturnValue(false)
  })

  it('should check if file exists', () => {
    fs.existsSync.mockReturnValue(true)

    expect(helpers.fileExists(api, 'foobar')).toBe(true)

    fs.existsSync.mockReturnValue(false)

    expect(helpers.fileExists(api, 'foobar')).toBe(false)
  })

  it('should add an import to the data array', () => {
    fs.existsSync.mockReturnValue(true)

    const data = []

    helpers.addImport(api, 'foobar', data, 'variables', "'")
    helpers.addImport(api, 'fizzbuzz', data, 'lists', "'")

    expect(data.length).toBe(4)

    fs.existsSync.mockReturnValue(false)

    helpers.addImport(api, 'foobar1', data, 'variables', "'")
    helpers.addImport(api, 'fizzbuzz1', data, 'lists', "'")

    expect(data.length).toBe(4)
  })

  it('should add imports to the data array', () => {
    fs.existsSync.mockReturnValue(true)

    const data = []

    helpers.addImports(api, 'foobar', data, "';")

    expect(data.length).toBe(6)
  })

  it('should merge sass variable rules', () => {
    fs.existsSync.mockReturnValue(true)

    const opt = {}

    helpers.mergeRules(api, opt, 'sass')

    expect(opt).toMatchSnapshot()

    const opt2 = {}

    helpers.mergeRules(api, opt2, 'scss')

    expect(opt2).toMatchSnapshot()
  })
})

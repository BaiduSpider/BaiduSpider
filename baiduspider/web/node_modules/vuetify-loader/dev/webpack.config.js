var path = require('path')
var webpack = require('webpack')
const VueLoaderPlugin = require('vue-loader/lib/plugin')
const VuetifyLoaderPlugin = require('vuetify-loader/lib/plugin')
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin

const isProd = process.env.NODE_ENV === 'production'

function sassLoaderOptions (indentedSyntax = false) {
  return {
    implementation: require('sass'),
    prependData: `@import "~@/_variables.scss"` + (indentedSyntax ? '' : ';'),
    sassOptions: { indentedSyntax },
  }
}

module.exports = {
  devtool: 'source-map',
  mode: isProd ? 'production' : 'development',
  entry: './src/main.js',
  output: {
    path: path.resolve(__dirname, './dist'),
    publicPath: '/dist/',
    filename: 'build.js'
  },
  module: {
    rules: [
      {
        test: /\.vue$/,
        loader: 'vue-loader',
      },
      {
        test: /\.js$/,
        loader: 'babel-loader',
        exclude: /node_modules\/(?!(vuetify)\/)/
      },
      {
        test: /\.sass$/,
        use: [
          'vue-style-loader',
          'css-loader',
          { loader: 'sass-loader', options: sassLoaderOptions(true) }
        ]
      },
      {
        test: /\.scss$/,
        use: [
          'vue-style-loader',
          'css-loader',
          { loader: 'sass-loader', options: sassLoaderOptions() }
        ]
      },
      {
        test: /\.(png|jpe?g|gif|svg|eot|ttf|woff|woff2)(\?.*)?$/,
        loader: 'url-loader',
        options: { limit: 8000 }
      }
    ]
  },
  resolve: {
    alias: {
      'vue$': path.resolve(__dirname, './node_modules/vue/dist/vue.runtime.esm.js'),
      '@': path.resolve(__dirname, 'src')
    },
    extensions: ['*', '.js', '.vue', '.json']
  },
  plugins: [
    new VueLoaderPlugin(),
    new VuetifyLoaderPlugin({
      progressiveImages: true
    }),
    new BundleAnalyzerPlugin({
      analyzerMode: 'static',
      openAnalyzer: false
    })
  ],
  devServer: {
    historyApiFallback: true,
    noInfo: true,
    overlay: true
  },
  performance: {
    hints: false
  },
  optimization: {
    concatenateModules: false
  }
}

if (isProd) {
  module.exports.devtool = '#source-map'
  // http://vue-loader.vuejs.org/en/workflow/production.html
  module.exports.plugins = (module.exports.plugins || []).concat([
    new webpack.DefinePlugin({
      'process.env': {
        NODE_ENV: '"production"'
      }
    })
  ])
}

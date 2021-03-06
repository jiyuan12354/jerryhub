var webpack = require('webpack')
var BundleTracker = require('webpack-bundle-tracker')

var config = require('./webpack.config.base.js')


// Add HotModuleReplacementPlugin and BundleTracker plugins
config.plugins = config.plugins.concat([
  new webpack.HotModuleReplacementPlugin(),
  // new webpack.NoErrorsPlugin(),
  new BundleTracker({filename: 'webpack/webpack-stats-local.json'}),
])

config.mode = 'development';

config.devtool = 'source-map';

module.exports = config

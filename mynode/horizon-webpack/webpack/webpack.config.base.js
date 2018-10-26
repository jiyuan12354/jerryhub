var path = require("path")

var local_address = "10.3.50.197"
module.exports = {
  context: __dirname,
  entry: [
    path.resolve('./frontend/src/index.jsx')
  ],

  output: {
    path: path.resolve('./assets/bundles/'),
    filename: '[name]-[hash].js',
    publicPath: 'http://'+ local_address +':8080/assets/bundles/', // Tell django to use this URL to load packages and not use STATIC_URL + bundle_name
  },

  plugins: [],

  devServer: {
    public: 'http://'+ local_address +':8080/',
    noInfo: false
  },

  module: {
    rules: [
      {
        test: /\.jsx?$/,
        exclude: /node_modules/,
        loader: 'babel-loader',
      },
      {
        test: /\.s?css$/,
        loaders: ['style-loader', 'css-loader', 'sass-loader']
      }
    ]
  },

  resolve: {
    extensions: ['.js', '.jsx']
  }
}
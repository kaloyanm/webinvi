const path = require('path');
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');
const UglifyJSPlugin = require('uglifyjs-webpack-plugin');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const autoprefixer = require('autoprefixer');
const cssnano = require('cssnano');

module.exports = function(env){
  const isDev = true;

  let webpackConfig = {
    context: __dirname,
    entry: {
      'core/static/core/dist/public': './public.js',
      'invoices/static/invoices/js/app': './app.js'
    },
    output: {
      path: path.resolve('./'),
      filename: '[name].js'
    },
    resolve: {
      modules: ['bower_components', 'node_modules'],
      extensions: ['.js']
    },
    module: {
      rules: [
        {
          test: /\.scss$/,
          loader: ExtractTextPlugin.extract({
            fallback : 'style-loader',
            use: [
              'css-loader',
              {
                loader: 'postcss-loader',
                options: {
                  plugins: [
                    autoprefixer({
                      browsers: [
                        'last 2 versions'
                      ]
                    })
                  ]
                }
              },
              {
                loader: 'sass-loader',
                query: {
                  sourceMap: isDev
                }
              }
            ]
          })
        }
      ]
    },
    plugins: [
      //new BundleTracker({filename: './webpack-stats.json'}),
      //new UglifyJSPlugin(),
      new ExtractTextPlugin(isDev ? 'style.dev.css' : 'style.css'),
      new webpack.ProvidePlugin({
        jQuery: 'jquery',
        $: 'jquery'
      })
    ]
  };

  return webpackConfig;
};

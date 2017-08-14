const path = require('path');
const webpack = require('webpack');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const autoprefixer = require('autoprefixer');
const cssnano = require('cssnano');

module.exports = function(env){
  const environment = env.arg;
  const isDev = environment === 'development';

  return {
    context: __dirname,
    entry: {
      'core/static/core/js/public': './core/assets/webpack-entry.public.js',
      'invoices/static/invoices/js/app': './core/assets/webpack-entry.app.js'
    },
    output: {
      path: path.resolve('./'),
      filename: '[name].js'
    },
    devtool: isDev ? 'source-map' : false,
    resolve: {
      modules: ['bower_components', 'node_modules'],
      extensions: ['.js'],
      alias: {
        vue$: 'vue/dist/vue.esm.js'
      }
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
                loader: 'postcss-loader'
              },
              {
                loader: 'sass-loader',
                options: {
                  sourceMap: isDev
                }
              }
            ]
          })
        }
      ]
    },
    plugins: [
      new webpack.DefinePlugin({
        'process.env.NODE_ENV': JSON.stringify(environment)
      }),
      //new BundleTracker({filename: './webpack-stats.json'}),
      new ExtractTextPlugin('./core/static/core/css/style.css'),
      new webpack.ProvidePlugin({
        jQuery: 'jquery',
        $: 'jquery',
        html2canvas: 'html2canvas',
        jsPDF: 'jspdf'
      })
    ]
  };
};

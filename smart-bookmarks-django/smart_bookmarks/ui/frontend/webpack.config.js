const path = require('path');
const ProvidePlugin = require('webpack/lib/ProvidePlugin');

module.exports = {
    mode: 'development',
    devtool: 'inline-source-map',
    entry: {
        main: [
            path.resolve('./src', 'js/index.js'),
        ],
        vendor: [
            'jquery',
        ],
    },
    output: {
        filename: '[name].bundle.js',
        path: path.resolve(__dirname, '../static/dist'),
    },
    plugins: [
        new ProvidePlugin({
          jQuery: 'jquery',
          $: 'jquery',
          jquery: 'jquery'
        }),
    ]
};

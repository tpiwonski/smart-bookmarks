const path = require('path');

module.exports = {
    entry: {
        ajax: './src/ajax.js',
        bookmark: './src/bookmark.js',
        toasts: './src/toasts.js',
    },
    output: {
        filename: '[name].bundle.js',
        path: path.resolve(__dirname, 'dist'),
    },
};

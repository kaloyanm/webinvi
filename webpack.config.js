const path = require('path');

module.exports = {
    entry: {
        main: [
            './node_modules/jquery/dist/jquery.min.js',
            './node_modules/bootstrap/dist/js/bootstrap.min.js',
            './node_modules/popper.js/dist/popper.min.js',
            './node_modules/html2canvas/dist/html2canvas.min.js',
            './node_modules/jspdf/dist/jspdf.min.js'
        ]
    },
    output: {
        path: path.resolve(__dirname, 'src/core/static/core/dist/'),
        filename: 'invoice.bundle.js'
    }
};
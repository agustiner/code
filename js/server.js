'use strict'

function serve_files(app, express) {
    app.use('/', express.static('public'));
}

module.exports = {
    serve_files: serve_files
}

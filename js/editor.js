'use strict'

const fs = require('fs')

function receive_edits(app) {
    app.post('/edit', function (req, res) {
	fs.writeFileSync('./public/' + req.body.page + '.json', JSON.stringify(req.body.path_list))
	res.sendStatus(200);
    })
}

module.exports = {
    receive_edits: receive_edits
}

'use strict'

const fs = require('fs')

function delete_node(node) {
    const nodes_file = fs.readFileSync('./public/nodes.json')
    var nodes_dict = JSON.parse(nodes_file.toString())

    if (node in nodes_dict) {
	delete nodes_dict[node]
	fs.writeFileSync('./public/nodes.json', JSON.stringify(nodes_dict))
    }

    if (fs.existsSync('./public/' + node + '.json') ) {
	fs.unlinkSync('./public/' + node + '.json')
    }

    if (fs.existsSync('./public/' + node)) {
	fs.unlinkSync('./public/' + node)
    }
}

function receive_deletes(app) {
    app.post('/delete', function (req, res) {
	delete_node(req.body.node)
	res.sendStatus(200);
    })
}

module.exports = {
    receive_deletes: receive_deletes
}

'use strict'

const fs = require('fs')

function delete_node(node) {
    const nodes_file = fs.readFileSync('./public/nodes.json')
    var nodes_dict = JSON.parse(nodes_file.toString())

    if (node in nodes_dict) {
	console.log('Deleting node', node)
	delete nodes_dict[node]
	fs.writeFileSync('./public/nodes.json', JSON.stringify(nodes_dict))
    }

    if (fs.existsSync('./public/' + node + '.json') ) {
	console.log('Deleting json', node)
	fs.unlinkSync('./public/' + node + '.json')
    }

    if (fs.existsSync('./public/' + node)) {
	console.log('Deleting png', node)
	fs.unlinkSync('./public/' + node)
    }
}

function receive_deletes(app) {
    app.post('/delete', function (req, res) {
	if (req.body.prompt == 'greenchickadee') {
	    delete_node(req.body.node)
	}
	res.sendStatus(200);
    })
}

module.exports = {
    receive_deletes: receive_deletes
}

'use strict'

const fs = require('fs')

function move_node(node, coordinate) {
    const nodesfile = fs.readFileSync('./public/nodes.json')
    var nodes_json = JSON.parse(nodesfile.toString())
    nodes_json[node] = coordinate
    nodes_json['last'] = coordinate
    fs.writeFileSync('./public/nodes.json', JSON.stringify(nodes_json))
}

function receive_moves(app) {
    app.post('/move', function (req, res) {
	if (req.body.prompt == 'greenchickadee') {
	    move_node(req.body.node, req.body.coordinate)
	}
	res.sendStatus(200);
    })
}

module.exports = {
    receive_moves: receive_moves
}

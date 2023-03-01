'use strict'

const fs = require('fs')

function move_node(node_list, xy_list) {
    const nodesfile = fs.readFileSync('./public/nodes.json')
    var nodes_json = JSON.parse(nodesfile.toString())

    for (var i = 0; i < node_list.length; i++) {
	nodes_json[node_list[i]] = xy_list[i]
    }
    
    nodes_json['last'] = xy_list[0]
    fs.writeFileSync('./public/nodes.json', JSON.stringify(nodes_json))
}

function receive_moves(app) {
    app.post('/move', function (req, res) {
	move_node(req.body.node_list, req.body.xy_list)
	res.sendStatus(200);
    })
}

module.exports = {
    receive_moves: receive_moves
}

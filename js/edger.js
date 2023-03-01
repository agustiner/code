'use strict'

const fs = require('fs')

function edge_node(edge_from_node, to_list) {
    var filename = './public/edges.json'
    var edgesfile = fs.readFileSync(filename)
    var edges_dict = JSON.parse(edgesfile.toString())
    edges_dict[edge_from_node] = to_list
    fs.writeFileSync(filename, JSON.stringify(edges_dict))
}

function receive_edges(app) {
    app.post('/edge', function (req, res) {
	if (req.body.prompt == 'greenchickadee') {
	    edge_node(req.body.edge_from_node, req.body.to_list)
	}
	res.sendStatus(200);
    })
}

module.exports = {
    receive_edges: receive_edges
}

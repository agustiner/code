'use strict'
const fs = require('fs')

function edge_node(node_list, edge_list) {
    var filename = './public/edges.json'
    var edgesfile = fs.readFileSync(filename)
    var edges_dict = JSON.parse(edgesfile.toString())

    for (var i = 0; i < node_list.length; i++) {
	edges_dict[node_list[i]] = edge_list[i]
    }
    fs.writeFileSync(filename, JSON.stringify(edges_dict))
}

function receive_edges(app) {
    app.post('/edge', function (req, res) {
	edge_node(req.body.node_list, req.body.edge_list)
	res.sendStatus(200);
    })
}

module.exports = {
    receive_edges: receive_edges
}

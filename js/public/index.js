var edge_first_node = ''
var bool_move_node = false
var bool_make_edge = false
var bool_move_connected_nodes = false
var bool_delete_edge = false
var bool_mobile = /iPhone|iPad/i.test(navigator.userAgent);
var move_node_names = []
var move_node_initial_coordinates = []

function set_json(url, payload) {
    var request = new XMLHttpRequest()
    request.open('POST', url, false)
    request.setRequestHeader('Content-Type', 'application/json')
    request.send(JSON.stringify(payload))
}

function get_json(url) {
    var request = new XMLHttpRequest()
    request.open('GET', url, false)
    request.send(null)
    return JSON.parse(request.responseText)
}

var nodes = get_json('/nodes.json')
var edges = get_json('/edges.json')

function delete_node(nodename) {
    payload = {
        node: nodename
    }

    set_json('/delete', payload)    
}

function move_node(nodename, coordinate) {
    payload = {
        node: nodename,
	coordinate: coordinate
    }

    set_json('/move', payload)
}

function edge_node(nodename, to_node_list) {
    payload = {
	from_node: nodename,
	to_node_list: to_node_list
    }

    set_json('/edge', payload)
}

async function update() {
    nodes = get_json('/nodes.json')
    edges = get_json('/edges.json')
    draw()
}

function stop_dragging(node) {
    bool_move_node = false
    move_node_names = []
    move_node_initial_coordinates = []
    deck_object.setProps({controller: true})
}

function set_move_node_names(parent_node) {
    var move_node_queue = []

    if (parent_node in edges) {
	move_node_queue = edges[parent_node]
    }

    while (move_node_queue.length > 0) {
	var next_node = move_node_queue.shift()
	if (!(move_node_names.includes(next_node))) {
	    move_node_names.push(next_node)
	    move_node_initial_coordinates.push(nodes[next_node])
	    if (next_node in edges) {
		move_node_queue.push(...edges[next_node])
	    }
	}
    }
}

function gettooltip({object}) {
    if (object == null || bool_mobile || bool_move_node || bool_make_edge || bool_delete_edge) {
        return
    }

    if (object[0].endsWith("png")) {
	return {
            html: `<img style="position:fixed;transform: translate(-50%, -50%);max-width:500px;max-height:300px;" src='${object[0]}'></img>`,
            style: {
		backgroundColor: "transparent"
            }
	}	
    } else {
	return {
            html: `<iframe src="http://agu.st/page.html?page=${object[0]}" style="pointer-events:none;border:none;position:fixed;transform:translate(-50%, -50%);width:900px;height:500px;"></img>`,
            style: {
		backgroundColor: "transparent"
            }
	}		
    }
}

function ondragstart(info, event) {
    if (info.object != null && bool_move_node == false) {
	bool_move_node = true
	deck_object.setProps({controller: false})
	move_node_names = [info.object[0]]
	move_node_initial_coordinates = [nodes[info.object[0]]]
	
	if (bool_move_connected_nodes) {
	    set_move_node_names(info.object[0])
	}
    }
}

function ondrag(info, event) {
    if (info.coordinate != null && info.object != null && bool_move_node == true) {
	var initial_coordinate = move_node_initial_coordinates[0]
	var move_delta = [initial_coordinate[0] - info.coordinate[0], initial_coordinate[1] - info.coordinate[1]]
	for (var i = 0; i < move_node_names.length; i++) {
	    nodes[move_node_names[i]] = [move_node_initial_coordinates[i][0] - move_delta[0], move_node_initial_coordinates[i][1] - move_delta[1]]
	}	
        draw()	
    } else if (info.coordinate == null && bool_move_node == true) {
	delete_node(move_node_names[0])
	stop_dragging()
	update()
    }
}

function ondragend(info, event) {
    if (info.object != null && bool_move_node == true) {
	for (var i = 0; i < move_node_names.length; i++) {
	    move_node(move_node_names[i], nodes[move_node_names[i]])
	}	
	stop_dragging()
	update()
    }
}

function onclick(info, event) {
    if (info.object != null) {
	if (info.object[0].endsWith('png')) {
	    window.open(info.object[0])
	} else {
	    window.open('/page.html?page=' + info.object[0])
	}
	
    } else if (info.object == null && event.leftButton == true) {
	move_node(String(Math.floor(new Date() / 1000)), info.coordinate)
	update()
    }
}

function onhover(info, event) {
    if (bool_make_edge && info.object != null) {
	if (edge_first_node == '') {
	    edge_first_node = info.object[0]
	    
	} else if (edge_first_node != '' && edge_first_node != info.object[0]) {
	    var edge_second_node = info.object[0]

	    if (!(edge_first_node in edges)) {
		edges[edge_first_node] = []
	    }
		
	    if (!(edge_second_node in edges)) {
		edges[edge_second_node] = []
	    }
	    
	    if (!(edges[edge_first_node].includes(edge_second_node))) {
		edges[edge_first_node].push(edge_second_node)
		edges[edge_second_node].push(edge_first_node)
		
		edge_node(edge_first_node, edges[edge_first_node])
		edge_node(edge_second_node, edges[edge_second_node])

		edge_first_node = ''
		update()
	    }
	}
    } else if (bool_delete_edge && info.object != null) {
	for (var neighbor of edges[info.object[0]]) {
	    neighbor_edges = edges[neighbor]
	    neighbor_edges.splice(neighbor_edges.indexOf(info.object[0]), 1)
	    edges[neighbor] = neighbor_edges
	    edge_node(neighbor, neighbor_edges)
	}
	edge_node(info.object[0], [])
	update()
    }
}

function draw() {
    var nodearray = []

    for (const [key, value] of Object.entries(nodes)) {
	if (key != 'last') {
	    nodearray.push([key, value[0], value[1]])
	}
    }

    const nodelayer = new deck.ScatterplotLayer({
	data: nodearray,
        getPosition: x => [x[1], x[2]],
        pickable: true,
        radiusMinPixels: 6
    })

    var edgearray = []

    for (const [node_from, nodes_to] of Object.entries(edges)) {
	var coordinate_from = nodes[node_from]

	for (const node_to of nodes_to) {
	    var coordinate_to = nodes[node_to]
	    edgearray.push([node_from, coordinate_from, coordinate_to])
	}
    }

    const edgelayer = new deck.LineLayer({
        data: edgearray,
	getSourcePosition: x => [x[1][0], x[1][1]],
	getTargetPosition: x => [x[2][0], x[2][1]],
	widthMinPixels: 1
    })

    deck_object.setProps({layers: [nodelayer, edgelayer]})
}

const deck_object = new deck.Deck({
    initialViewState: {
        longitude: nodes['last'][0],
	latitude: nodes['last'][1],
        zoom: 15
    },
    controller: true,
    getCursor: () => 'default',
    getTooltip: gettooltip,
    onClick: onclick,
    onDrag: ondrag,
    onDragEnd: ondragend,
    onDragStart: ondragstart,
    onHover: onhover,
    onLoad: draw,
    pickingRadius: 15,
})

function keydown(e) {
    if (e.code == 'Space') {
	bool_make_edge = !bool_make_edge
	edge_first_node = ''
    } else if (e.code == 'KeyM') {
	bool_move_connected_nodes = !bool_move_connected_nodes
    } else if (e.code == 'KeyD') {
	bool_delete_edge = !bool_delete_edge
    } else if (e.code == 'KeyR') {
	update()
    }
}

document.addEventListener('contextmenu', event => event.preventDefault())
document.addEventListener('keydown', keydown)

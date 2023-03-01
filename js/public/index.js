var bool_delete_edge = false
var bool_draw = false
var bool_make_edge = false
var bool_move_connected_nodes = false
var bool_scroll = false
var bool_tooltip = false
var bool_mobile = /iPad/i.test(navigator.userAgent)
var current_page = ''
var drag_first_y = 0
var edge_first_node = ''
var edit_timeout_id = 0
var move_nodes = []
var edge_nodes = []
var pages = {}
var draw_scale = 1
var canvas = document.getElementById('page')
canvas.width = window.innerWidth
canvas.height = window.innerHeight
canvas.style.width = canvas.width + "px"
canvas.style.height = canvas.height + "px"
canvas.width = canvas.width * window.devicePixelRatio
canvas.height = canvas.height * window.devicePixelRatio
var context = canvas.getContext('2d')
var original_transform = context.getTransform()
context.lineWidth = 3

function get_json(url) {
    var request = new XMLHttpRequest()
    request.open('GET', url, false)
    request.send(null)
    return JSON.parse(request.responseText)
}

async function get_graph_data() {
    nodes = get_json('/nodes.json')
    edges = get_json('/edges.json')
    draw_graph()
}

function set_json(url, payload) {
    var request = new XMLHttpRequest()
    request.open('POST', url, false)
    request.setRequestHeader('Content-Type', 'application/json')
    request.send(JSON.stringify(payload))
}

function delete_node(nodename) {
    payload = {
        node: nodename
    }

    set_json('/delete', payload)    
}

function set_node_xy(node_list, xy_list) {
    payload = {
        node_list: node_list,
	xy_list: xy_list
    }

    set_json('/move', payload)
}

function set_node_edges(node_list, edge_list) {
    payload = {
	node_list: node_list,
	edge_list: edge_list
    }

    set_json('/edge', payload)
}

function edit() {
    var payload = {
	page: current_page,
	path_list: pages[current_page]
    }
    set_json('/edit', payload)
}

function set_move_nodes(move_node_queue) {
    move_nodes = []
    while (move_node_queue.length > 0) {
	var next_node = move_node_queue.shift()
	if (!(move_nodes.includes(next_node))) {
	    move_nodes.push(next_node)
	    if (next_node in edges) {
		move_node_queue.push(...edges[next_node])
	    }
	}
    }
}

function ondragstart(info, event) {
    if (info.object != null) {
	deck_object.setProps({controller: false})
	
	if (bool_move_connected_nodes) {
	    set_move_nodes([info.object[0]])
	} else {
	    move_nodes = [info.object[0]]
	}
    }
}

function stop_dragging() {
    deck_object.setProps({controller: true})
    move_nodes = []
    get_graph_data()
}

function ondragend(info, event) {
    if (move_nodes.length > 0 && info.coordinate != null) {
	var initial_xy = nodes[move_nodes[0]]
	var delta_xy = [initial_xy[0] - info.coordinate[0], initial_xy[1] - info.coordinate[1]]

	var move_nodes_xy = []
	
	for (var i = 0; i < move_nodes.length; i++) {
	    var move_node_x = nodes[move_nodes[i]][0] - delta_xy[0]
	    var move_node_y = nodes[move_nodes[i]][1] - delta_xy[1]
	    var move_node_xy = [move_node_x, move_node_y]
	    move_nodes_xy.push(move_node_xy)
	}
	set_node_xy(move_nodes, move_nodes_xy)
	stop_dragging()
	
    } else if (move_nodes.length > 0 && info.coordinate == null) {
	delete_node(move_nodes[0])
	stop_dragging()
    }
}

function onclick(info, event) {
    if (info.object != null) {
	if (info.object[0].endsWith('png')) {
	    window.open(info.object[0])
	} else {
	    get_page(info.object[0])
	}
	
    } else if (info.object == null && event.leftButton == true) {
	set_node_xy([String(Math.floor(new Date() / 1000))], [info.coordinate])
	get_graph_data()
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

		if (!(edge_first_node in edge_nodes)) {
		    edge_nodes.push(edge_first_node)
		}

		if (!(edge_second_node in edge_nodes)) {
		    edge_nodes.push(edge_second_node)
		}
		
		edge_first_node = edge_second_node
	    }
	}
	draw_graph()
	
    } else if (bool_delete_edge && info.object != null) {	
	for (var neighbor of edges[info.object[0]]) {
	    edges[neighbor].splice(edges[neighbor].indexOf(info.object[0]), 1)
	    edges[info.object[0]] = []

	    if (!(info.object[0] in edge_nodes)) {
		edge_nodes.push(info.object[0])
	    }

	    if (!(neighbor in edge_nodes)) {
		edge_nodes.push(neighbor)
	    }
	}
	draw_graph()
    }
}

function draw_graph() {
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
	var xy_from = nodes[node_from]

	for (const node_to of nodes_to) {
	    var xy_to = nodes[node_to]
	    edgearray.push([node_from, xy_from, xy_to])
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

function get_graph() {
    document.getElementById('graph').style.display = 'inline'
    document.getElementById('page').style.display = 'none'
}

function get_page_data(node) {
    if (!(node in pages)) {
	var request = new XMLHttpRequest()
	request.open('GET', node + '.json', false)
	request.send(null)
	if (request.status == 200) {
	    pages[node] = JSON.parse(request.responseText)
	} else {
	    pages[node] = []
	}
    }
}

function get_page(node) {
    context.setTransform(original_transform)
    document.getElementById('graph').style.display = 'none'
    document.getElementById('page').style.display = 'inline'
    current_page = node
    get_page_data(node)
    draw_page()
}

function get_xy(event) {
    var inverse_transform = context.getTransform().invertSelf()
    var x = inverse_transform.a * event.pageX * window.devicePixelRatio + inverse_transform.c * event.pageY * window.devicePixelRatio + inverse_transform.e
    var y = inverse_transform.b * event.pageX * window.devicePixelRatio + inverse_transform.d * event.pageY * window.devicePixelRatio + inverse_transform.f
    return [x, y]
}

function add_point(event) {
    var [x, y] = get_xy(event)
    pages[current_page][pages[current_page].length - 1].push([x, y])
}

function draw_page() {
    context.fillStyle = 'white'
    context.fillRect(0, - context.getTransform().f, canvas.width, canvas.height)
    context.fillStyle = 'black'

    for (var i = 0; i < pages[current_page].length; i++) {
	context.beginPath()
	for (var j = 0; j < pages[current_page][i].length - 1; j++) {
	    context.lineTo(pages[current_page][i][j][0] * draw_scale, pages[current_page][i][j][1] * draw_scale)
	}
	context.stroke()
    }
}

function keydown(e) {
    if (e.code == 'Space') {
	bool_delete_edge = false
	bool_tooltip = false
	bool_move_connected_nodes = false
	bool_make_edge = !bool_make_edge
    } else if (e.code == 'KeyM') {
	bool_move_connected_nodes = !bool_move_connected_nodes
	bool_delete_edge = false
	bool_make_edge = false
	bool_tooltip = false
    } else if (e.code == 'KeyD') {
	bool_delete_edge = !bool_delete_edge
	bool_tooltip = false
	bool_move_connected_nodes = false
	bool_make_edge = false
    } else if (e.code == 'KeyT') {
	bool_tooltip = !bool_tooltip
	bool_move_connected_nodes = false
	bool_delete_edge = false
	bool_make_edge = false
    }

    if (edge_nodes.length > 0) {
	edge_first_node = ''
	var node_edges = []
	
	for (node of edge_nodes) {
	    node_edges.push(edges[node])
	}

	set_node_edges(edge_nodes, node_edges)
	edge_nodes = []	
    }
}

function schedule_edit() {
    clearTimeout(edit_timeout_id)
    edit_timeout_id = setTimeout(edit, 5000)
}

function is_tap(event) {
    if (Math.abs(event.pageY - drag_first_y) < 1) {
	return true
    }    
    return false
}

function gettooltip({object}) {
    if (object == null || !bool_tooltip) {
        return
    }

    if (object[0].endsWith("png")) {
       return {
            html: `<img style="position:fixed;transform: translate(-50%, -50%);max-width:500px;max-height:300px;" src='/${object[0]}'></img>`
       }       
    } else {
       current_page = object[0]
       get_page_data(object[0])
       draw_page()
       var page = document.getElementById('page')
       var dataurl = page.toDataURL()
       return {
           html: `<img style="width:800px;position:fixed;transform: translate(-50%, -50%)" src='${dataurl}'></img>`
       }
    }
}

document.addEventListener('keydown', keydown)

canvas.addEventListener('click', function(event) {
    get_graph()
})
 
canvas.addEventListener('touchstart', function (event) {
    if (event.touches && event.touches[0].touchType == 'stylus') {
	bool_draw = true
	pages[current_page].push([])
	add_point(event)
    } else if (event.touches && event.touches[0].touchType == 'direct') {
	bool_scroll = true
	drag_first_y = event.pageY
    }
})

canvas.addEventListener('touchmove', function (event) {
    event.preventDefault()
    if (bool_draw) {
	add_point(event)
    } else if (bool_scroll) {
	var drag_diff_y = event.pageY - drag_first_y
	context.translate(0, drag_diff_y / 10)
	draw_page()
    }
})

canvas.addEventListener('touchend', function (event) {
    if (bool_draw) {
	bool_draw = false
	add_point(event)
	draw_page()
	schedule_edit()	
    } else if (bool_scroll) {
	bool_scroll = false
	if (is_tap(event)) {
	    get_graph()
	}
    }
})

canvas.onwheel = function (event) {
    context.translate(0, event.wheelDelta / 2)
    draw_page()
}

if (!bool_mobile) {
    draw_scale = 0.5
}

var nodes = get_json('/nodes.json')
var edges = get_json('/edges.json')

const deck_object = new deck.Deck({
    id: 'graph',
    initialViewState: {
        longitude: nodes['last'][0],
	latitude: nodes['last'][1],
        zoom: 15
    },
    controller: true,
    getTooltip: gettooltip,
    onClick: onclick,
    onDragEnd: ondragend,
    onDragStart: ondragstart,
    onHover: onhover,
    onLoad: draw_graph,
    pickingRadius: 13,
})

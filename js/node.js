"use strict";

const express = require('express')
const app = express()
app.use(express.json({limit: '50mb'}));

const server = require('./server.js')
server.serve_files(app, express)

const mover = require('./mover.js')
mover.receive_moves(app)

const deleter = require('./deleter.js')
deleter.receive_deletes(app)

const edger = require('./edger.js')
edger.receive_edges(app)

const editor = require('./editor.js')
editor.receive_edits(app)

const port = 8001

app.listen(port, () => {
    console.log(`Listening on port ${port}.`)
})

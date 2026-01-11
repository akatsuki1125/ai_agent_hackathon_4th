const ws = require("ws")
const wss = new ws.WebSocketServer({port:8765})

wss.on("connection", function connection(ws){
    ws.on("error", console.error);
    ws.on("message", function message(data){
        console.log(`received: ${data}`)
    })
    ws.send("connected")
})
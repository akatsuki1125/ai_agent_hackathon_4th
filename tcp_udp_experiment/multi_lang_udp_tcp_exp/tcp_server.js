const net = require("net")

var adress = '127.0.0.1';
var port = 8008;

const server = net.createServer((socket) => {
    console.log("client connected", socket.remoteAddress, socket.remotePort);

    socket.on("data", (data) => {
        console.log("received bytes:", data.length);
        console.log("received data:", data.toString("utf8"));
    })

    socket.on("end", (data) => {
        console.log("client disconnected");
    })
})

server.listen(port, adress, () => {
    console.log(`listening on ${adress}:${port}`);
})
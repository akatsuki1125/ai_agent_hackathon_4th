const dgram = require("dgram");

const ADDR = '127.0.0.1';
const PORT = 8008;

const server = dgram.createSocket("udp4");

server.on("message", (msg, rinfo) => {
    console.log("received bytes", msg.length);
    console.log("received data", msg);
})

server.bind(PORT, ADDR, () => {
    console.log(`listening on ${ADDR}:${PORT}`);
})
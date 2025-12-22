const dgram = require("dgram")

const ADDR = '127.0.0.1';
const PORT = 8008;

client = dgram.createSocket("udp4")

const data = Buffer.from("aiueo", "ascii")
client.send(data, PORT, ADDR, (err) => {
    if (err) console.error("send error", e)
    client.close()
})
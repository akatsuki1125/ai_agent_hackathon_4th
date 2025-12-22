const net = require("net");

var adress = '127.0.0.1';
var port = 8008;

const client = net.connect({host:adress, port:port}, () => {
    console.log("connected");
    //const data = Buffer.alloc(100, 0x00);
    //const data = "hello world"
    const data = "こんにちは"
    //client.write(data);
    client.write(data, "utf8");
    client.end()
});


client.on("error", (err) => {
    console.error("error:", err.message);
})
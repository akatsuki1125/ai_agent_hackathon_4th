import dgram from "dgram";

const HOST = "127.0.0.1";
const PORT = 5005;
const FPS  = 30;

const socket = dgram.createSocket("udp4");
let seq = 0;

console.log(`[udp_client.js] sending to ${HOST}:${PORT} fps=${FPS}`);

setInterval(() => {
  const msg = {
    cid: "JS",
    seq: seq,
    ts: Date.now() / 1000.0,
    payload: "x".repeat(200)
  };

  const buf = Buffer.from(JSON.stringify(msg));
  socket.send(buf, PORT, HOST);
  seq++;
}, 1000 / FPS);


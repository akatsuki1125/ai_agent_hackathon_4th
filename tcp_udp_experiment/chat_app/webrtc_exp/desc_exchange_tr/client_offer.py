from websockets.asyncio.client import connect
import asyncio
import time
from aiortc import RTCPeerConnection, RTCSessionDescription
import json

async def offer():
    pc = RTCPeerConnection()
    dc = pc.createDataChannel("chat")
    offer = await pc.createOffer()
    await pc.setLocalDescription(offer)
    return pc.localDescription


async def main():
    cnt = 0
    async with connect("ws://127.0.0.1:8765") as websocket:
        desc = await offer()
        payload = {"type": desc.type, "sdp": desc.sdp}
        print("send")
        await websocket.send(json.dumps(payload))
        msg = await websocket.recv()
        print(msg)
        cnt += 1
        await time.sleep(100)

asyncio.run(main())
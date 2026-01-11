from websockets.asyncio.client import connect
import asyncio
import time
from aiortc import RTCPeerConnection, RTCSessionDescription
import json

async def main():
    cnt = 0
    async with connect("ws://127.0.0.1:8765") as websocket:
        payload = await websocket.recv()
        offer = RTCSessionDescription(payload["sdp"], payload["type"])

        pc = RTCPeerConnection()
        await pc.setRemoteDescription(offer)
        answer = await pc.createOffer()
        desc = await pc.setLocalDescription(answer)

        payload = {"type": desc.type, "sdp": desc.sdp}
        await websocket.send(payload)

asyncio.run(main())
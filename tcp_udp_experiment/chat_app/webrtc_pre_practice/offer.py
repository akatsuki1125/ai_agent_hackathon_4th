from websockets.asyncio.client import connect
import asyncio
import time
from aiortc import RTCPeerConnection, RTCSessionDescription
import json

async def main():
    isConnected = False
    async with connect("ws://127.0.0.1:8765") as websocket:
        while not isConnected:
            pc = RTCPeerConnection()
            dc = pc.createDataChannel("chat")

            @dc.on("open")
            def on_open():
                print("opened")
                dc.send("hello from offer")

            offer = await pc.createOffer()
            await pc.setLocalDescription(offer)
            desc = pc.localDescription

            payload = {"user": "offer", "desc_sdp": desc.sdp, "desc_type": desc.type}
            print("send")
            await websocket.send(json.dumps(payload))

            while True:
                msg = await websocket.recv()
                #print(type(msg))
                msg = json.loads(msg)
                #print(type(msg))
                print("make_connection")
                answer_desc = RTCSessionDescription(sdp=msg[1], type=msg[0])
                await pc.setRemoteDescription(answer_desc)
                isConnected = True
                break

        @dc.on("open")
        def openmes():
            print("opend_2")
            dc.send("hello from offer")
            print("send to answer")

        await asyncio.sleep(10)

asyncio.run(main())
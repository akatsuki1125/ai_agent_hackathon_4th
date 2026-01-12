from websockets.asyncio.client import connect
import asyncio
import time
from aiortc import RTCPeerConnection, RTCSessionDescription
import json


async def main():
    isFirst = True
    async with connect("ws://127.0.0.1:8765") as websocket:
        if isFirst:
            pc = RTCPeerConnection()

            @pc.on("datachannel")
            def on_datachannel(channel):
                print("datachannel received:", channel.label)

                @channel.on("message")
                def on_message(message):
                    print(message)

            await websocket.send(json.dumps({"user":"answer"}))
            while True:
                msg = await websocket.recv()
                print(msg)
                print(type(msg))
                break

            msg = json.loads(msg)
            #print(f"msg: {msg}")
            #print(type(msg))
            offer_desc = RTCSessionDescription(sdp=msg[1], type=msg[0])
            await pc.setRemoteDescription(offer_desc)
            #print("remote_set")

            answer = await pc.createAnswer()
            await pc.setLocalDescription(answer)

            desc = pc.localDescription
            print("local_set")
            payload = {"user": "answer", "desc_type": desc.type, "desc_sdp": desc.sdp}

        await websocket.send(json.dumps(payload))
        print("sdp_send")

        # @dc.on("open")
        # def opened():
        #     print("opened")

        # @dc.on("message")
        # def get_msg(message):
        #     print(message)
        await asyncio.sleep(100)



asyncio.run(main())

from websockets.asyncio.client import connect
import asyncio
import time
from aiortc import RTCPeerConnection, RTCSessionDescription
import json


async def main():
    async with connect("ws://127.0.0.1:8765") as websocket:

        payload = await websocket.send("aaa")
        payload = await websocket.recv()
        payload = json.loads(payload)
        print(f"payload: {payload}")

        for k,v in payload.items():
            if v!="aaa":
                key = k
                val = json.loads(v)
                payload = {k:json.loads(v)}

        print(f"payload: {payload}")
        payload = val
        print(f"payload: {payload}")

        offer_desc = RTCSessionDescription(sdp=payload["sdp"], type=payload["type"])
        pc = RTCPeerConnection()
        await pc.setRemoteDescription(offer_desc)

        print("search icecandidates")
        @pc.on("icegatheringstatechange")
        def on_state():
            print("ice state:", pc.iceGatheringState)


        @pc.on("icecandidate")
        def on_icecandidate(candidate):
            print("call_back_called.")
            if candidate is None:
                print("candidate is not here.")
                return
            print("candidate is here.")
            asyncio.create_task(send_candidate(candidate))

        async def send_candidate(candidate):
            print(candidate)
            await websocket.send(json.dumps(candidate))


        answer = await pc.createAnswer()
        await pc.setLocalDescription(answer)
        await asyncio.sleep(10)

        desc = pc.localDescription
        #print(f"desc: {desc}")
        print(pc.localDescription.sdp)
        #print(pc.on("icecandidate"))
        payload = {"type": desc.type, "sdp": desc.sdp}
        await websocket.send(json.dumps(payload))

        print("finished")
        @pc.on("datachannel")
        def printdeta():
            print(pc.data)

asyncio.run(main())

# このまま書くのは，俺の理解の範疇を超えている．．．かもしれない
# とりあえず，両方に Description が揃うところまでを実装してみるか？
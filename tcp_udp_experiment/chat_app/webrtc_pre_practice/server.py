import asyncio
from websockets.asyncio.server import serve
import json

name_list = ["nanashi", "hachimitsu", "neko", "inu", "girrafe"]
clients = {}
desks = {}
websockets = set()


async def echo(websocket):
    if websocket not in websockets:
        print(f"new connection from: {websocket}")
        websockets.add(websocket)
        desks[websocket] = "no_set"

    async for message in websocket:
        message = json.loads(message)
        #print(message)
        #print(type(message))
        if message["user"]=="offer":
            if desks[websocket] == "no_set":
                print("[start] set descriptinon from offer")
                desks[websocket] = (message["desc_type"], message["desc_sdp"])
                clients["offer"] = websocket
                print("[complete] set descriptinon from offer")

        if message["user"]=="answer":
            print(f"connection_from_answer {message}")
            if desks[websocket] == "no_set":
                desks[websocket] = "wait_for_offer"
                await websocket.send(json.dumps(desks[clients["offer"]]))
                continue
            if desks[websocket] == "wait_for_offer":
                print(f"recv_from_ans: {message}")
                desks[websocket] = (message["desc_type"], message["desc_sdp"])
                await clients["offer"].send(json.dumps(desks[websocket]))
        
        print(desks)


async def main():
    async with serve(echo, "127.0.0.1", port=8765) as server:
        await server.serve_forever()


asyncio.run(main())

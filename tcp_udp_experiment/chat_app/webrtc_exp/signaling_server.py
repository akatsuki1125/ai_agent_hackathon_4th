import asyncio
from websockets.asyncio.server import serve
import uuid

client_list = set()
users = {}
descs = {}

async def echo(websocket):
    async for message in websocket:
        await websocket.send(message)
        if websocket not in client_list:
            client_list.add(websocket)
            users[websocket] = uuid.uuid1()
            print(users)


async def main():
    async with serve(echo, "127.0.0.1", port=8765) as server:
        await server.serve_forever()

asyncio.run(main())
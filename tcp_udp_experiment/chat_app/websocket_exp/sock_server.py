import asyncio
from websockets.asyncio.server import serve 

def sync_echo(websocket):
    for message in websocket:
        websocket.send(message)
        print(message)

async def echo(websocket):
    async for message in websocket:
        await websocket.send(message)
        print(message)

async def main():
    async with serve(echo, "127.0.0.1", port=8765) as server:
        await server.serve_forever()

asyncio.run(main())
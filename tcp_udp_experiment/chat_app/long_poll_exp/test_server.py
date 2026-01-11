import asyncio
import websockets

async def handler(ws):
    async for msg in ws:
        #print(msg)
        print(msg, end="", flush=True)
        await ws.send(msg)

async def main():
    async with websockets.serve(handler, "127.0.0.1", 8765):
        await asyncio.Future()

asyncio.run(main())
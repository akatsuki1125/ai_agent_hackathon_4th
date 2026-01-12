import asyncio
from websockets.asyncio.client import connect

async def main():
    async with connect("ws://127.0.0.1:8765") as con:
        async def recv_loop():
            async for res_ms in con:
                #res_ms = await con.recv()
                if res_ms != "":
                    print(res_ms)
        
        asyncio.create_task(recv_loop())
        loop = asyncio.get_running_loop()

        while True:
            ms = await loop.run_in_executor(None, input)
            if ms == "q":
                return
            if ms != "":
                await con.send(ms)
                ms = ""


asyncio.run(main())
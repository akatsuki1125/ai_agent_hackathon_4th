import asyncio
from websockets.asyncio.server import serve

async def echo(websocket):
    #print(type(websocket))
    #print(websocket)
    # ルーム設定みたいなのは，確かにあったほうが便利な気がしてきた
    # 送る相手を明示しないところがちょっと難しいな，というかサーバーから無理やり送りつけるのは無理なんだろ？
    async for message in websocket:
        print(websocket, message)
        await websocket.send("<< "+message+" >>")

async def main():
    async with serve(echo, "127.0.0.1", port=8765) as server:
        await server.serve_forever()
        # ここに await が入っていないと動かない理由は？？
        # server.serve_forever が終わるまで待たないから．．．？

asyncio.run(main())
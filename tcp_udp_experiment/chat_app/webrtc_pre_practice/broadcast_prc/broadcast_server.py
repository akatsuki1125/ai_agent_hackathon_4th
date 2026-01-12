import asyncio
from websockets.asyncio.server import serve

name_list = ["nanashi", "hachimitsu", "neko", "inu", "girrafe"]
clients = {}
websockets = set()
# 送る側も json じゃないとめんどくさいという話になってくるが．．．
# これがプロトコル設計すらさせられるしんどさというやつか．．．？

async def echo(websocket):
    if websocket not in websockets:
        websockets.add(websocket)
        clients[websocket] = "default"
        await websocket.send("From_Server: send_me_user_id")

    async for message in websocket:
        if clients[websocket] == "default":
            clients[websocket] = message
            await websocket.send("From_Server: your_id_resislated. please send message.")
        else:
            print(f"user: {websocket}")
            print(f"message: {message}")
            print(f"clients: {websockets}")
            for client in websockets:
                if client != websocket:
                    await client.send(f"<< {clients[websocket]}: {message} >>")
                # await client.send(f"<< {clients[client]}: {message} >>")
                # これにすると，クライアント各々の名前で帰ってしまう．なんか変な感じだが？
                # いやまあ，あるクライアントが送信してきたのをそのタイミングで発火して返してるので，悪くはないのか

async def main():
    async with serve(echo, "127.0.0.1", port=8765) as server:
        await server.serve_forever()

asyncio.run(main())
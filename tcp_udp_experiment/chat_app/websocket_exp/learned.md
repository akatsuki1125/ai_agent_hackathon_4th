# websocket_exp 学びメモ

## WebSocket の基礎
- WebSocket は最初に HTTP Upgrade を行い、その後は同じ接続で双方向通信する。
- 接続を張り直さないので `[S]`（SYN）が毎回出るわけではない。

## Python websockets（async 版）
- ライブラリが asyncio 前提なので `async/await` が必須。
- `async for` は「次のメッセージが来るまで待つ」ループ。

```py
import asyncio
import websockets

async def echo(ws):
    async for msg in ws:
        await ws.send(msg)
        print(msg)

async def main():
    async with websockets.serve(echo, "127.0.0.1", 8765):
        await asyncio.Future()

asyncio.run(main())
```

## Python websockets（sync 版）
- `websockets.sync` を使えば asyncio なしで動く。
- ただし送受信の同時処理はスレッドが必要になりがち。

```py
from websockets.sync.client import connect
import time

with connect("ws://127.0.0.1:8765") as ws:
    ws.send("hello")
    print(ws.recv())
    time.sleep(1)
```

## async/await の理解（議論まとめ）
- `await` は「待つべき非同期処理」で制御をイベントループに返す。
- `await` を付けない非同期関数は「実行されない（コルーチンを作るだけ）」。
- `await` なしの `while` ループはイベントループを止める。

```py
async def loop():
    while True:
        await asyncio.sleep(0)  # ここで制御を返す
```

## 1文字入力（termios/tty）
- Enter を待たずに1文字ずつ読む。

```py
import sys, tty, termios

fd = sys.stdin.fileno()
old = termios.tcgetattr(fd)
try:
    tty.setcbreak(fd)
    while True:
        ch = sys.stdin.read(1)
        if ch == "q":
            break
        print("got:", ch)
finally:
    termios.tcsetattr(fd, termios.TCSADRAIN, old)
```

## tcpdump で WebSocket 確認
- Upgrade ヘッダや接続維持を確認できる。

```bash
sudo tcpdump -i lo0 -s 0 -A 'tcp port 8765'
```

## ロングポーリング（議論の要点）
- サーバーは更新が来るまで返さない。
- クライアントは返ってきたらすぐ次を投げる。

```js
function longpoll() {
  fetch("/poll")
    .then(res => res.text())
    .then(data => {
      if (data === "") return setTimeout(longpoll, 1000);
      console.log(data);
      longpoll();
    });
}
longpoll();
```

## 同期 vs 非同期の使い分け（議論まとめ）
- async は I/O 待ちが多いときに有利。
- 同期で並行にしたいならスレッドを使う。
- どちらも使い分けの問題で、目的に応じて選ぶ。

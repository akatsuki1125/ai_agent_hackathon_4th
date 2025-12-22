# TCP 学習メモ（ここまで）

## クライアント側の基本
- TCP は「コネクションを張ってから送る」ストリーム型通信
- 送信は `sendall(bytes)` が基本（`bytes` を渡す）
- `socket.socket()` を使う場合は `connect()` が必要
- `socket.create_connection((host, port))` は接続済みソケットを返す
- `socket` と `create_connection` はどちらか片方だけ使えば OK

## サーバー側の基本
- `bind()` → `listen()` → `accept()` → `recv()` の順
- `listen()` は待受開始するだけで即戻る
- 実際に接続を待つのは `accept()`
- 受信は `accept()` が返す `conn` に対して `recv()` する（`skt.recv` ではない）
- `recv()` は必ずバッファサイズ引数が必要（例: `recv(1024)`）

## よく出たエラーと原因
- `ValueError: too many values to unpack`
  - `create_connection` に `(host, port)` のタプルを渡していなかった
- `OSError: [Errno 49] Can't assign requested address`
  - `bind` に自分のPCに存在しないIPを指定していた
  - ローカルなら `127.0.0.1`、外部公開なら `0.0.0.0`
- `Permission denied`
  - 0〜1023 の特権ポートを使っていた（例: 40）
  - 1024以上に変更が必要
- `recv() takes at least 1 argument`
  - `recv` の引数（バッファサイズ）を忘れていた
- `OSError: [Errno 57] Socket is not connected`
  - `listen` 用ソケットに `recv` していた（`conn.recv` が正しい）

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

## 接続の作り方のバリエーション
- サーバー側は `socket.create_server((host, port))` で bind+listen をまとめられる
- クライアント側は `socket.socket()` で作って `connect()` する方法も動作確認済み
- `connect()` の戻り値は `None` なので、送信はソケット本体に対して行う

## tcpdump で見えたこと
- `Flags [S]` → SYN、`[S.]` → SYN+ACK、`[P.]` → データ送信、`[F.]` → FIN
- `options [...]` に TCP オプション（`mss`, `wscale`, `TS`, `sackOK` など）が出る
- `length 100` は payload サイズ。`-X` で本文の hex/ASCII 表示が見える
- 送信データが `b"\x00"*100` だと本文は `00` が並ぶ
- ASCII 可視文字で送ると `tcpdump -X` の ASCII 欄で確認できる

## TCP オプション（tcpdump で見た範囲）
- `mss N`: 最大セグメントサイズ（TCPペイロード上限）
- `wscale N`: ウィンドウスケール（受信ウィンドウの倍率）
- `TS val X ecr Y`: タイムスタンプ（送信値/エコー値）
- `sackOK`: 選択的ACK対応
- `nop`: オプションのパディング
- `eol`: オプション終端

## tcpdump 1行の読み取り例
```
14:29:19.328462 IP 127.0.0.1.54153 > 127.0.0.1.8008: Flags [S], seq 2451870180, win 65535, options [mss 16344,nop,wscale 6,nop,nop,TS val 3459161528 ecr 0,sackOK,eol], length 0
```
- `14:29:19.328462`: パケットの捕捉時刻（ローカル時刻）
- `IP`: IPv4 パケット
- `127.0.0.1.54153 > 127.0.0.1.8008`: 送信元IP:ポート → 宛先IP:ポート
- `Flags [S]`: SYN（接続開始）
- `seq 2451870180`: 送信側の初期シーケンス番号（ISN）
- `win 65535`: 受信ウィンドウサイズ（相手に通知する受信可能量）
- `options [...]`: TCPオプション
  - `mss 16344`: 最大セグメントサイズ
  - `wscale 6`: ウィンドウスケール（2^6 倍）
  - `TS val 3459161528 ecr 0`: タイムスタンプ
  - `sackOK`: SACK対応
  - `nop`: パディング
  - `eol`: オプション終端
- `length 0`: ペイロードなし（SYNは通常データを持たない）

## tcpdump コマンド例とオプションの意味
```
tcpdump -i lo0 -nn -X -S tcp port 8008
```
- `-i lo0`: ループバックインターフェース（localhost）を監視
- `-nn`: 逆引き/名前解決をしない（IP/ポートを数値で表示）
- `-X`: payload を hex + ASCII で表示
- `-S`: シーケンス番号を絶対値で表示（相対表示ではない）
- `tcp port 8008`: 8008番ポートの TCP 通信に絞り込むフィルタ

## シーケンス番号と ACK の理解
- `ack N` は「次に欲しいバイト番号」を表す
- 100バイト送れば seq/ack は 100 進む
- FIN は 1バイト消費するため ACK が +1 される
- `tcpdump` のデフォルトは相対 seq 表示
- `-S` を付けると絶対 seq が見える（初期値が大きいのは仕様）

## UDP で観測できたこと
- UDP は接続確立/ACK/FIN がないので、送信1回がほぼ1パケットに対応する
- `tcpdump -X udp port 8008` で payload がそのまま見える
- 送信データが大きい場合は IP フラグメントが起きる可能性がある
- TCPはセグメント化して再構成されるが、UDPは順序や再送が保証されない

## 乱れの観測に関する理解
- 送信側でシャッフル/ドロップを入れると「UDPの性質を擬似的に再現」できる
- ネットワーク由来の乱れを観測したい場合は送信側は弄らず、経路や環境を変えて測る
- ローカル環境では乱れが出にくいので、遠隔・Wi-Fi・混雑時間帯などが有効

## 3way ハンドシェイクと行数が多くなる理由
- 3way ハンドシェイクは SYN → SYN+ACK → ACK の3パケット
- その後にデータ送信（P.）と ACK が続く
- 切断時は FIN/ACK の往復が入るため行数が増える
- tcpdump の例では「接続確立 + データ + 切断」で合計 8〜10 行程度になる
- 場合によっては ACK が余分に見えることがあり、行数が増えることがある

## 3way ハンドシェイクの具体例（一般形）
```
client -> server: Flags [S]     seq X
server -> client: Flags [S.]    seq Y, ack X+1
client -> server: Flags [.]     ack Y+1
```
- `X`, `Y` はそれぞれの初期シーケンス番号（ISN）
- この3本が揃うと TCP 接続が確立する

## 自分の tcpdump の具体例（今回のログ）
```
127.0.0.1.51126 > 127.0.0.1.8008: Flags [S],  seq 2198399826
127.0.0.1.8008  > 127.0.0.1.51126: Flags [S.], seq 2715995905, ack 2198399827
127.0.0.1.51126 > 127.0.0.1.8008: Flags [.],  ack 2715995906
```
- 1行目が SYN（接続開始）
- 2行目が SYN+ACK（応答）
- 3行目が ACK（接続確立）

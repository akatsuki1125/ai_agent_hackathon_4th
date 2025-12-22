# TCP/UDP 実験 まとめ（現状）

## 目的
- TCP/UDP の挙動差を体感するため、連番付きフレーム送受信の最小実験を作成。
- 将来的な WebRTC（ビデオ通話）に向け、RTP 的要素（seq, timestamp, frame rate）を意識。

## 現状の構成

### 1) Python UDP サーバ（受信側）
- ファイル: `udp_server.py`
- 役割: UDP 受信、seq 欠損の概算・片道遅延・受信レート表示
- 受信データ: JSON（UTF-8）
  - 必須: `seq` (int), `ts` (float)
  - 任意: `cid` (str), `payload` (str)
- バインド: `0.0.0.0:5005`
- 主要観測値:
  - `one_way_ms = (recv_time - ts) * 1000`
  - 欠損は `last_seq` 差分で概算

### 2) Python UDP クライアント（送信側）
- ファイル: `udp_client.py`
- 役割: 指定 host:port に一定 fps で JSON フレーム送信
- 例:
  - `uv run udp_server.py`
  - `uv run udp_client.py --host 127.0.0.1 --fps 30`
- 送信パラメータ:
  - `--host` 必須
  - `--port` デフォルト 5005
  - `--fps` デフォルト 50
  - `--size` payload サイズ
  - `--drop` 擬似ロス（0〜1）
  - `--delay_ms` 擬似遅延
- 注意: `--cid` は初期版に未実装（必要なら追加）

### 3) Node.js UDP クライアント（JavaScript）
- ファイル: `udp_client.js`
- 役割: Python サーバへの UDP 送信で互換性確認
- `dgram` 使用（npm install 不要）
- `MODULE_NOT_FOUND` はファイル名 typo が原因（`udp_clinent.js`）
  - `mv udp_clinent.js udp_client.js` で解決済み

## ハマりポイントと解決
- (A) `--cid` が unrecognized
  - 原因: `udp_client.py` に引数定義がない
  - 対応: `parser.add_argument("--cid", ...)` を追加し JSON に `cid` を入れる
- (B) `node udp_client.js` が MODULE_NOT_FOUND
  - 原因: ファイル名 typo
  - 対応: `mv udp_clinent.js udp_client.js`

## uv / 依存関係
- Python UDP 実装は標準ライブラリのみ
- `uv add` は不要

## 現時点で確認できたこと
- UDP でフレーム（seq, ts, payload）を一定周期で送信
- 受信側で以下を観測可能
  - `fps`
  - 欠損（seq gap）
  - `one_way_ms`（ts 差）
- Python サーバに対し Python/Node の両方から送信できることを確認

## これからの拡張方針（合意済み）
- 画像より音声が簡単（フレーム区切り、欠損許容、WebRTC と相性）
- ブラウザで扱う場合の経路
  - TCP 的: WebSocket
  - UDP 的: WebRTC

### 次にやる候補
1. サーバ側の表示改善（cid 別に fps/loss/latency）
2. TCP 比較（同じフレームを TCP で送信）
3. WebRTC 導入（WebSocket で音声フレーム送受信→後で置換）

## Codex に渡す最低仕様（プロトコル）

送信する JSON フレーム:
```json
{
  "cid": "A",
  "seq": 123,
  "ts": 1730000000.123,
  "payload": "xxxxx..."
}
```

- UDP サーバ: `0.0.0.0:5005`
- 観測指標: `fps`, `loss_rate`（seq gap）, `one_way_ms`（ts 差）

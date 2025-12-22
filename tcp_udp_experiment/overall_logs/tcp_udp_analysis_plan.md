# Plan_v2

TCP/UDP の基礎理解に加えて、並列送信・大きいデータの順序/破損・リアルタイム監視・HTTP の基礎まで含めた拡張検証プラン。既存の UDP 実験をベースに、観測指標をそろえて比較できる状態を目指す。

## Requirements
- TCP/UDP の接続・経路・パケット処理の違いを言語化できること
- WebRTC/WebSocket の位置づけ（層・目的・特性）を理解できること
- 既存の UDP 実験で観測できる指標を整理して使えること
- HTTP の基本（GET/POST の違い）を整理できること
- 並列送信・大きいデータ送信・リアルタイム監視の観測ができること
- 複数言語で同様の実装ができること

## Scope
- In: TCP/UDP の仕組み、通信特性、距離/サイズ/ロスへの影響、WebRTC/WebSocket の比較、HTTP の基本（GET/POST）、複数言語での実装
- Out: 実運用設計（NAT 越えの詳細、暗号スイート詳細、TURN 構築など）

## Files and entry points
- `udp_tcp_exp/udp_server.py`
- `udp_tcp_exp/udp_client.py`
- `udp_tcp_exp/tcp_server.py`
- `udp_tcp_exp/tcp_client.py`
- `udp_exp/udp_server.py`
- `udp_exp/udp_client.py`

## Data model / API changes
- なし（理解・検証メイン）

## Action items
[ ] TCP と UDP の基本フローをまとめる（接続確立、信頼性、順序保証、再送、輻輳制御）
[ ] WebRTC/WebSocket を「層・目的・転送方式」で整理する（WebRTC=UDPベースのリアルタイム、WebSocket=TCP上の双方向）
[ ] 既存 UDP 実験の観測指標（fps/loss/one_way_ms）とプロトコル特性の対応表を作る
[ ] データサイズ・送信レート・遅延/ロスでどのように結果が変わるか仮説を立てる
[ ] 小さな実験シナリオ（ローカル/同一LAN/遠距離）を定義する
[ ] 並列送信（複数クライアント同時送信）での挙動を観測する
[ ] 大きいデータ送信時の順序・欠損・破損の傾向を観測する
[ ] リアルタイム通信の監視指標（レート、遅延、欠損）を整理する
[ ] HTTP の GET/POST の違い（用途、キャッシュ、ボディ、冪等性）を整理する
[ ] 複数言語で同じ通信実験を実装して違いを整理する
[ ] Docker を使わない前提でのネットワーク構成（ルータ/NAT/ポート開放）を整理する
[ ] まとめとして「用途別に TCP/UDP/WebRTC/WebSocket を選ぶ基準」を箇条書き化する

## Action items (advanced)
[ ] Docker/コンテナのネットワーク構成（ブリッジ/NAT/ポート公開）の挙動を整理する
[ ] ngrok のトンネル構造とファイアウォール/NAT 回避の仕組みを整理する
[ ] TCP 輻輳制御（CUBIC など）がOSで自動適用されることを確認する
[ ] 輻輳シミュレーション（帯域制限・遅延・ロス）を無料ツールで実施する
[ ] UDPの順序乱れ/欠損を遠隔環境で観測し、再現性を評価する
[ ] Bluetooth 通信の観測可否を整理する（macOS / Linux実機 / Raspberry Pi）
[ ] Bluetooth スニファの有無で観測範囲が変わる点を整理する

## Testing and validation
- 既存 UDP 実験を使って指標が変化することを確認（fps/loss/one_way_ms）
- TCP 版（後続で実装する場合）と比較できる観測ポイントを定義

## Risks and edge cases
- 片道遅延は時刻同期がないと絶対値がズレる（相対変化を見る）
- ローカル環境では差が出にくく、結論が単純化されがち
- NAT/Firewall 影響は概念理解に留める必要がある
- 大きいデータは UDP だとフラグメント依存になる

## Open questions
- まずは「概念整理」を優先するか、「小実験」を先に回すかどちらが良いか
- 実験対象の距離（ローカル/LAN/外部）をどこまで広げるか








# Plan

TCP/UDP の基本動作と、WebRTC/WebSocket との違いを「概念理解」と「小さな実験」で確認するための学習・検証プラン。既存の UDP 実験コードを使い、プロトコルの性質と距離・データサイズの影響を整理する。

## Requirements
- TCP/UDP の接続・経路・パケット処理の違いを言語化できること
- WebRTC/WebSocket の位置づけ（層・目的・特性）を理解できること
- 既存の UDP 実験で観測できる指標を整理して使えること
- HTTP の基本（GET/POST の違い）を整理できること

## Scope
- In: TCP/UDP の仕組み、通信特性、距離/サイズ/ロスへの影響、WebRTC/WebSocket との比較、HTTP の基本（GET/POST）
- Out: 実運用設計（NAT 越えの詳細、暗号スイート詳細、TURN 構築など）

## Files and entry points
- `udp_exp/udp_server.py`
- `udp_exp/udp_client.py`
- `udp_exp/README.md`（ある場合の説明確認）

## Data model / API changes
- なし（理解・検証メイン）

## Action items
[ ] TCP と UDP の基本フローをまとめる（接続確立、信頼性、順序保証、再送、輻輳制御）
[ ] WebRTC/WebSocket を「層・目的・転送方式」で整理する（WebRTC=UDPベースのリアルタイム、WebSocket=TCP上の双方向）
[ ] 既存 UDP 実験の観測指標（fps/loss/one_way_ms）とプロトコル特性の対応表を作る
[ ] データサイズ・送信レート・遅延/ロスでどのように結果が変わるか仮説を立てる
[ ] 小さな実験シナリオ（ローカル/同一LAN/遠距離）を定義する
[ ] 並列送信（複数クライアント同時送信）での挙動を観測する
[ ] 大きいデータ送信時の順序・欠損・破損の傾向を観測する
[ ] リアルタイム通信の監視指標（レート、遅延、欠損）を整理する
[ ] HTTP の GET/POST の違い（用途、キャッシュ、ボディ、冪等性）を整理する
[ ] まとめとして「用途別に TCP/UDP/WebRTC/WebSocket を選ぶ基準」を箇条書き化する

## Testing and validation
- 既存 UDP 実験を使って指標が変化することを確認（fps/loss/one_way_ms）
- TCP 版（後続で実装する場合）と比較できる観測ポイントを定義

## Risks and edge cases
- 片道遅延は時刻同期がないと絶対値がズレる（相対変化を見る）
- ローカル環境では差が出にくく、結論が単純化されがち
- NAT/Firewall 影響は概念理解に留める必要がある

## Open questions
- まずは「概念整理」を優先するか、「小実験」を先に回すかどちらが良いか
- 実験対象の距離（ローカル/LAN/外部）をどこまで広げるか

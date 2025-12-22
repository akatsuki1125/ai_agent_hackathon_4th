# Plan

TCP/UDP の基本動作と、WebRTC/WebSocket との違いを「概念理解」と「小さな実験」で確認するための学習・検証プラン。既存の UDP 実験コードを使い、プロトコルの性質と距離・データサイズの影響を整理する。

## Requirements
- TCP/UDP の接続・経路・パケット処理の違いを言語化できること
- WebRTC/WebSocket の位置づけ（層・目的・特性）を理解できること
- 既存の UDP 実験で観測できる指標を整理して使えること

## Scope
- In: TCP/UDP の仕組み、通信特性、距離/サイズ/ロスへの影響、WebRTC/WebSocket との比較
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

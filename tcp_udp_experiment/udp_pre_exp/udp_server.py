#!/usr/bin/env python3
import json
import socket
import time

HOST = "0.0.0.0"
PORT = 5005
BUF = 65535  # UDP max-ish

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))
    print(f"[udp_server] listening on {HOST}:{PORT}")

    last_seq = None
    received = 0
    lost = 0
    start = time.time()

    while True:
        data, addr = sock.recvfrom(BUF)
        now = time.time()

        try:
            msg = json.loads(data.decode("utf-8"))
            seq = int(msg["seq"])
            ts = float(msg["ts"])  # sender timestamp (sec)
        except Exception as e:
            print(f"[udp_server] parse error from {addr}: {e}")
            continue

        received += 1
        one_way_ms = (now - ts) * 1000.0

        if last_seq is not None and seq != last_seq + 1:
            gap = seq - (last_seq + 1)
            if gap > 0:
                lost += gap

        last_seq = seq

        if received % 50 == 0:
            elapsed = now - start
            rate = received / elapsed if elapsed > 0 else 0.0
            loss_rate = (lost / (received + lost)) if (received + lost) > 0 else 0.0
            print(
                f"[udp_server] recv={received} lost≈{lost} "
                f"loss_rate≈{loss_rate:.3f} one_way≈{one_way_ms:.1f}ms rate≈{rate:.1f}fps "
                f"from={addr}"
            )

if __name__ == "__main__":
    main()


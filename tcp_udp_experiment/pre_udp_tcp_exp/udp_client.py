#!/usr/bin/env python3
import argparse
import json
import random
import socket
import time

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", required=True, help="server IP (e.g., 192.168.x.x)")
    parser.add_argument("--port", type=int, default=5005)
    parser.add_argument("--fps", type=float, default=50.0, help="frames per second")
    parser.add_argument("--size", type=int, default=200, help="payload bytes")
    parser.add_argument("--drop", type=float, default=0.0, help="client-side drop prob [0..1]")
    parser.add_argument("--delay_ms", type=float, default=0.0, help="client-side artificial delay per frame")
    args = parser.parse_args()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr = (args.host, args.port)

    interval = 1.0 / args.fps
    seq = 0
    payload = "x" * max(0, args.size)

    print(f"[udp_client] sending to {addr} fps={args.fps} size={args.size} drop={args.drop} delay_ms={args.delay_ms}")

    next_t = time.time()
    while True:
        now = time.time()
        if now < next_t:
            time.sleep(next_t - now)
        next_t += interval

        if args.delay_ms > 0:
            time.sleep(args.delay_ms / 1000.0)

        if args.drop > 0 and random.random() < args.drop:
            seq += 1
            continue

        msg = {"seq": seq, "ts": time.time(), "payload": payload}
        data = json.dumps(msg).encode("utf-8")
        sock.sendto(data, addr)
        seq += 1

if __name__ == "__main__":
    main()


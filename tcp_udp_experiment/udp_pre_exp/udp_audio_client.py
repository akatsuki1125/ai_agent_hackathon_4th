#!/usr/bin/env python3
import argparse
import base64
import json
import random
import socket
import time
import wave


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", required=True, help="server IP (e.g., 192.168.x.x)")
    parser.add_argument("--port", type=int, default=5005)
    parser.add_argument("--wav", required=True, help="path to mono/stereo WAV file")
    parser.add_argument("--chunk_ms", type=int, default=20, help="chunk duration in ms")
    parser.add_argument("--loop", action="store_true", help="loop WAV when it ends")
    parser.add_argument("--drop", type=float, default=0.0, help="client-side drop prob [0..1]")
    parser.add_argument("--delay_ms", type=float, default=0.0, help="client-side artificial delay per frame")
    args = parser.parse_args()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr = (args.host, args.port)

    with wave.open(args.wav, "rb") as wf:
        rate = wf.getframerate()
        channels = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        chunk_frames = max(1, int(rate * args.chunk_ms / 1000))
        chunk_bytes = chunk_frames * channels * sampwidth

        interval = args.chunk_ms / 1000.0
        seq = 0
        next_t = time.time()

        print(
            "[udp_audio_client] sending to "
            f"{addr} wav={args.wav} rate={rate} ch={channels} "
            f"sampwidth={sampwidth} chunk_ms={args.chunk_ms} bytes={chunk_bytes} "
            f"drop={args.drop} delay_ms={args.delay_ms} loop={args.loop}"
        )

        while True:
            now = time.time()
            if now < next_t:
                time.sleep(next_t - now)
            next_t += interval

            if args.delay_ms > 0:
                time.sleep(args.delay_ms / 1000.0)

            if args.drop > 0 and random.random() < args.drop:
                seq += 1
                wf.readframes(chunk_frames)
                continue

            frames = wf.readframes(chunk_frames)
            if not frames:
                if args.loop:
                    wf.rewind()
                    continue
                break

            payload_b64 = base64.b64encode(frames).decode("ascii")
            msg = {
                "seq": seq,
                "ts": time.time(),
                "payload": payload_b64,
                "rate": rate,
                "channels": channels,
                "sampwidth": sampwidth,
                "chunk_ms": args.chunk_ms,
            }
            data = json.dumps(msg).encode("utf-8")
            sock.sendto(data, addr)
            seq += 1


if __name__ == "__main__":
    main()

import sys
import tty
import termios
import asyncio
import websockets

async def main():
    uri = "ws://127.0.0.1:8765"

    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)

    try:
        tty.setcbreak(fd)
        async with websockets.connect(uri) as ws:
            while True:
                ch = sys.stdin.read(1)
                if ch == "q":
                    break
                print(f"got: {ch!r}")
                await ws.send(ch)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

asyncio.run(main())
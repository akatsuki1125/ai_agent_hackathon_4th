from websockets.sync.client import connect
import time

def hello():
    with connect("ws://127.0.0.1:8765") as websocket:
        cnt = 0
        while cnt < 10:
            websocket.send("hello_world!")
            recv = websocket.recv()
            print(f"recv_message: {recv}")
            cnt += 1
            time.sleep(1)

hello()
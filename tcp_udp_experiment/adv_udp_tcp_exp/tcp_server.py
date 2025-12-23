import socket

SERVER_ADDR = "127.0.0.1"
PORT = 8008

skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
skt.bind((SERVER_ADDR, PORT))
skt.listen(4)
skt.accept()

conn, addr = skt.accept()

rcv_datas = []
while True:
    buf = conn.recv(65536)

    print(f"recived size: {len(buf)}")
    print(f"recived data (20): {buf[:20]}...")

    if not buf:
        break

    rcv_datas.append(buf)

all_data = b"".join(rcv_datas)
print(f"recived size: {len(all_data)}")
print(f"recived data (20): {all_data[:20]}...")

with open("recieved_data/otani_recieved.mp4", "wb") as f:
    f.write(all_data)
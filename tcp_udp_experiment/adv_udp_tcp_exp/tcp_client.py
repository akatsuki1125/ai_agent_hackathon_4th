import socket

SERVER_ADDR = "127.0.0.1"
PORT = 8008

skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("start connection_establish")
connection = skt.connect((SERVER_ADDR, PORT))
print("finish connection_establish")

print("read_data")
with open("send_data/otani.mp4", "rb") as f:
    file_data = f.read()

#datasize = 100
data = file_data

print("send_packet")
skt.sendall(data)
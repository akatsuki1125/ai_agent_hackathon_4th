import socket

SERVER_ADDR = "127.0.0.1"
PORT = 8008

skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("start connection_establish")
connection = skt.connect((SERVER_ADDR, PORT))
print("finish connection_establish")

datasize = 100
data = bytes(range(0,100))

print("send_packet")
skt.sendall(data)
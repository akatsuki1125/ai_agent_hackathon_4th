import socket

SERVER_ADDR = "127.0.0.1"
PORT = 8008

skt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
skt.bind((SERVER_ADDR, PORT))

buf = skt.recvfrom(1024)

print(buf)
import socket

SERVER_ADDR = "127.0.0.1"
PORT = 8008

skt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #よくわからんが，方針の変更が必要らしい
datasize = 100

with open("lilycs/juves.txt", "r", encoding="utf-8") as f:
    text = f.read()

data = text.encode("utf-8")
print("send_packet")
skt.sendto(data, (SERVER_ADDR, PORT))
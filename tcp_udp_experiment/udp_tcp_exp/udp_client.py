import socket

SERVER_ADDR = "127.0.0.1"
PORT = 8008

#skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
skt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #よくわからんが，方針の変更が必要らしい
#DGRAM はデータグラム（datagra）の略
print("start connection_establish")
#skt.connect((SERVER_ADDR, PORT)) #UDP には必要ない

print("finish connection_establish")

datasize = 100
#data = b"\x00" * datasize #null datas   
#data = bytes(range(0,100))

with open("lilycs/juves.txt", "r", encoding="utf-8") as f:
    text = f.read()

data = text.encode("utf-8")

print("send_packet")
#connection.sendall(data)
#skt.sendall(data) 
skt.sendto(data, (SERVER_ADDR, PORT))
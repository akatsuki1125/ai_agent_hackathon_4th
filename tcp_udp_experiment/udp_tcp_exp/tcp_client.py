import socket

#SERVER_ADDR = "192.168.0.12" ローカルホストじゃないと多分無理っぽい？
SERVER_ADDR = "127.0.0.1"
#PORT = "40" #特権ポートなのでだめ（1 ~ 1023)，あと，数字で指定しよう
PORT = 8008

# socket の方か，connection の方かどっちかだけを使う，今回は connection だけでオッケー
skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("start connection_establish")
#connection = socket.create_connection(SERVER_ADDR, PORT) タプルで指定する必要あり
connection = socket.create_connection((SERVER_ADDR, PORT))
print("finish connection_establish")

datasize = 100
data = b"\x00" * datasize

print("send_packet")
connection.sendall(data)
import socket

#SERVER_ADDR = "192.168.0.12" #ローカルホストとかじゃないと多分無理っぽい
SERVER_ADDR = "127.0.0.1"
PORT = 8008

#skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#skt.bind((SERVER_ADDR, PORT))

#skt.listen(4)
#skt.accept()
skt = socket.create_server((SERVER_ADDR, PORT))
conn, addr = skt.accept()
buf = conn.recv(1024)

print(buf)


import socket

#この方法は 127.0.0.1 しかとってこれない
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
print(local_ip)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect(("8.8.8.8", 80))
local_ip = sock.getsockname()
sock.close()
print(local_ip[0])
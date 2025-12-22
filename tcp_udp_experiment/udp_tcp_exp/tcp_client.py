import socket

SERVER_ADDR = "192.168.0.12"

skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection = socket.create_connection(SERVER_ADDR)

socket.sendall(skt)
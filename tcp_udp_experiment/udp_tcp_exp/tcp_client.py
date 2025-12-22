import socket

SERVER_ADDR = "192.168.0.12"

skt = socket(socket.AF_INET, socket.SOCK_STREAM)
socket.create_connection(SERVER_ADDR)


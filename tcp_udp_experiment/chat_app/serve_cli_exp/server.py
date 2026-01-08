import requests

url = "http://127.0.0.1:8000"
port = 8000

message = None
isget = False

print("server start")
while not isget:
    message = requests.get(url)
    if message:
        isget = True

print(message)

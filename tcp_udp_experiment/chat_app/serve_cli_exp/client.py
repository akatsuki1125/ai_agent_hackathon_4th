import requests

url = "http://127.0.0.1:8000"
port = 8000

message = "fuck you"
requests.post(url, message)
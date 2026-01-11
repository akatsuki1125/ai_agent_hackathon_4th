import requests 

while True:
    c = input()
    print(c)
    requests.post("http://127.0.0.1:8000/send", c)
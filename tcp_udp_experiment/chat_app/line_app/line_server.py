from flask import Flask, request

app = Flask(__name__, static_folder=".", static_url_path="")

messages = []

@app.get("/")
def index():
    return app.send_static_file("line.html")

@app.post("/send")
def send():
    message = request.get_data(as_text=True)
    messages.append(message)
    return "", 200

@app.get("/get_messages")
def return_messages():
    print(messages)
    return messages

app.run(host="127.0.0.1", port=8000)
from flask import Flask, request, send_from_directory

app = Flask(__name__, static_folder=".", static_url_path="")
messages = []

# @app.get("/")
# def index():
#     return send_from_directory(".", "mini.html")

# @app.get("/mini.js")
# def js():
#     return send_from_directory(".", "mini.js")

@app.get("/")
def index():
    return app.send_static_file("mini.html")

@app.post("/msg")
def recv():
    #print(request.get_data(as_text=True))
    msg = request.get_data(as_text=True)
    messages.append(msg)
    print(msg)
    return "", 200

@app.get("/msgs")
def list_msgs():
    print(messages)
    return {"messages": messages}

app.run(host="127.0.0.1", port=8000)
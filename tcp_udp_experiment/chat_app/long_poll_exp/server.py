from flask import Flask, request
import time

app = Flask(__name__, static_url_path="", static_folder=".")

str_queue = ""

@app.get("/")
def main_page():
    return app.send_static_file("sock.html")

@app.get("/poll")
def polling():
    timeout = 20
    start = time.time()
    global str_queue
    while time.time()-start < timeout:
        if len(str_queue)>0:
            ret = str_queue[0]
            str_queue = str_queue[1:]
            return ret
        time.sleep(0.1)
    else:
        return ""

@app.post("/send")
def get_char():
    global str_queue
    text = request.get_data(as_text=True)
    str_queue += text
    #print(text)
    #print(str_queue)
    return "", 200

app.run("127.0.0.1", port=8000)
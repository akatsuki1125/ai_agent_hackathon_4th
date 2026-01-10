from flask import Flask, send_from_directory
import os

app = Flask(__name__, static_url_path="", static_folder=".")

titles = os.listdir("send_movies/")
print(titles)

# 普通に適当なサムネをとってそれを表示させるだけでも結構むずそうな予感
# 思考が一気にローレベルに落ちて悲しいが，まあそんなもんでしょ

@app.get("/")
def hello():
    return app.send_static_file("mov_list.html")

@app.get("/titles")
def send_titles():
    return titles #リストをそのまま返せるのか．．．？

@app.get("/movie")
def mov():
    return app.send_static_file("mov.html")

# これのルーティングをうまくやりたいところだが，いまいちやり方が思いつかないというか知らない
@app.get("/movie/sample")
def mov_send():
    return send_from_directory(directory=".", path="send_movies/mov_hts-samp002.mp4")
# id の同期がめんどくさそう，サーバー側とクライアント側で．どうにかならないもんか

app.run("127.0.0.1", port=8000)
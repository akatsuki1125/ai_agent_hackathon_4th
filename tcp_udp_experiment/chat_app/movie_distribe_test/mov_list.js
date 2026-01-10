//let titles = fetch("http://127.0.0.1:8000/titles")
//.then((titles) => console.log(titles.text()))
// pending が帰ってくる，なぜなら，.text() も promise を返すので．

// この書き方は，Promise を明示的に持ちたい時以外は特に使わん
let titles = fetch("http://127.0.0.1:8000/titles")
    .then(res => res.text()).then(text => console.log(text))

// console.log(titles) // この場合，こっちが先に実行させて promise pending が出てくる


fetch("http://127.0.0.1:8000/titles")
    .then(res => res.json())
    .then(text => console.log(text)) // 勝手に json になる，flask か python がリストとか辞書を勝手にそうしている

const titles_div = document.getElementById("titles")

// localhost と 127.0.0.1:8000 で普通に CROSが発動するので注意が必要
fetch("http://127.0.0.1:8000/titles")
    .then(res => res.json())
    .then(text => {
        sorted = [...text].sort()
        sorted.forEach(t => {
            div = document.createElement("div")
            div.textContent = t
            titles_div.appendChild(div)
        })
    }) 

// １ページに全動画を載せるか，それともページを分けるかという話 (まあ両パターン作ればいい)
// ホバーしたら，プレビューするみたいな機能があってもカッコいいが難しそう
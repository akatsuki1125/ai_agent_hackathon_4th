let movie_stage = document.getElementById("mov_stage")
movie_stage.style.width = "700px"
movie_stage.style.height = "500px"
movie_stage.style.backgroundColor = "gray"

let response_field = document.getElementById("mov_response")

let video = document.getElementById("video")
video.style.width = "650px"
video.style.height = "450px"
// fetch("http://127.0.0.1:8000/movie/sample")
//     .then(mov => {
//         console.log(mov)
//         mov.text()
//     }).then(text => {
//         response_field.textContent = text
//     })
// これでは response の中身を見れない，response の中身は真面目に一個ずつ取り出す必要ガール

fetch("http://127.0.0.1:8000/movie/sample")
    .then(res => 
        // console.log(res)
        // const blob = res.blob()
        // return {res, blob}  // まあなんかあかんらしい，関数に直で .then をつけないとその関数の実行終了を待ってくれない
        Promise.all([res, res.blob()])
    ).then(([res,blob]) => {
        return blob.arrayBuffer().then(buf => {
            const head = new Uint8Array(buf).slice(0,10)
            return [res, blob, head]
        })
    }).then(([res, blob, head]) => {
        // この辺の URL を作る謎は，ブラウザを使わない動画再生 app を作れば違いがわかりそう
        video.src = URL.createObjectURL(blob)
        console.log(blob)
        const info ={ 
            type: res.type,
            url: res.url,
            status: res.status,
            ok: res.ok,
            redirected: res.redirected,
            //text: res.text // text を送ってないので出てこない
            content_type: res.headers.get("content-type"),
            content_length: res.headers.get("content-length"),
            // content: res.content //こんなものは存在しないらしい
            blob_type: blob.type,
            blob_size: blob.size,
            blob_head: Array.from(head).join(","),
            video_path: video.src
        }
        return {info, res}
        //return info //object [object] みたいなカス表示が実現される
    }).then(ret => {
        const text = JSON.stringify(ret.info, null, 2)
        const res = ret.res
        response_field.textContent = text
    })
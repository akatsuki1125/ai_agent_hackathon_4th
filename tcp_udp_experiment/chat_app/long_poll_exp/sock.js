/** * @type {HTMLCanvasElement} */
const can = document.getElementById("canvas")
/** * @type {CanvasRenderingContext2D} */
const ctx = can.getContext("2d")

const input_area = document.getElementById("input_chars")
// むしろ，もう通信も全て html ページに表示して，ページ内で通信みたいなことはできないか？
// 流石に意味不明？だがそれでいい？

can.width = 500
can.height = 500
ctx.fillStyle = "#aaa"
ctx.fillRect(0,0,can.width, can.height)

function longpoll(){
    fetch("/poll")
        .then(res => res.text())
        .then(data => {
            input_area.textContent += data
            longpoll()
        })
        .catch(() => {
            setTimeout(longpoll, 1000)
        })
}

longpoll()
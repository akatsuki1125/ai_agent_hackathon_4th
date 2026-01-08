const button = document.getElementById("send")
const text = document.getElementById("msg")
const nameInput = document.getElementById("name")

button.addEventListener("click", ()=>{
    let div = document.createElement("div")
    let divn = document.createElement("div")
    div.textContent = text.value
    divn.textContent = nameInput.value
    document.body.appendChild(div)
    document.body.appendChild(divn)
    fetch("/msg", {
        method: "POST",
        body: text.value
    });
})

const fileInput = document.getElementById("file")
const preview = document.getElementById("preview");

fileInput.addEventListener("change", ()=>{
    const file = fileInput.files[0]
    let div = document.createElement("div")
    div.textContent = file.name
    document.body.appendChild(div)

    let img = document.createElement("img")
    img.src = URL.createObjectURL(file)
    console.log(img.src)

    preview.appendChild(img)
})
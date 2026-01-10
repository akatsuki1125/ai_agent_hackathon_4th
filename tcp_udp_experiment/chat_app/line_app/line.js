const send_button = document.getElementById("send")
const inputs = document.getElementById("input")
const chat_area = document.getElementById("chat_area");

sessionStorage.removeItem("user_id");
let userID = sessionStorage.getItem("user_id")
if(!userID){
    userID = crypto.randomUUID().slice(-5);
    sessionStorage.setItem("user_id", userID)
}

send_button.addEventListener("click", () => {
    console.log("clicked")
    let message = inputs.value
    const payload = {"user": userID, "text":message}
    fetch("/send", {
        method: "POST",
        body: JSON.stringify(payload)
    })
    inputs.value = ""
})

inputs.addEventListener("keydown", (e) => {
    if (e.isComposing) return;
    if (e.key === "Enter"){
        send_button.click()
        e.preventDefault()
    }
})

function show_messages(){
    messa
}

timeout = 1000
setInterval(() => {
    fetch("/get_messages")
    .then(res => res.json())
    .then(data => {
        chat_area.innerHTML="";
        console.log(data)
        messages = data
        messages.forEach(m => {
            let div = document.createElement("div")
            const obj = JSON.parse(m)
            if(obj["user"]===userID){
                div.className = "me"
            }else{
                div.className = "else"
            }
            div.textContent = obj["user"] + ": " + obj["text"]
            chat_area.appendChild(div)
        });
    })
    //console.log(messages)
}, timeout);
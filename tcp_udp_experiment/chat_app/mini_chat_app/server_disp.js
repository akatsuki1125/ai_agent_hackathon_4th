const div = document.getElementById("logs")

async function refresh(){
    const res = await fetch("/msgs")
    const data = await res.json();

    div.innerHTML = ""
    data.messages.forEach((m) => {
        const d = document.createElement("div")
        d.textContent = m;
        div.appendChild(d)
    });
}

setInterval(refresh, 1000)
refresh();
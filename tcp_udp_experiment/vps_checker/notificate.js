const WEBHOOK_URL=process.env.SLACK_WEBHOOK_URL

async function send(){
    const now = new Date().toISOString();
    const ip = require("os").networkInterfaces()["en0"][1]["address"]

    let response = await fetch(WEBHOOK_URL, {
                        method: "POST",
                        headers: {"Content-Type": "application/json"},
                        body: JSON.stringify({"text": `hello from javascript\nip_address:${ip}`})
                    })

    const status = response.status
    const text = await response.text()

    console.log(status, text)

    require("fs").appendFileSync("post_check.log", `\n${now}: ${status} ${text} \nip_address:${ip}`)
}

console.log(require("os").networkInterfaces()["en0"][1]["address"])

send()
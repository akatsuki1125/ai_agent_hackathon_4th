const WEBHOOK_URL=process.env.SLACK_WEBHOOK_URL

async function send(){
    let response = await fetch(WEBHOOK_URL, {
                        method: "POST",
                        headers: {"Content-Type": "application/json"},
                        body: JSON.stringify({"text": "hello from javascript"})
                    })

    const status = response.status
    const text = await response.text()

    console.log(status, text)

    const now = new Date().toISOString();
    require("fs").appendFileSync("post_check.log", `\n${now}: ${status} ${text}`)
}

send()
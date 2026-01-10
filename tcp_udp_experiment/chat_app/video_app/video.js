let video = document.getElementById("video")
let audio = document.getElementById("audio")
let video_button = document.getElementById("video_button")
let audio_button = document.getElementById("audio_button")

video_button.addEventListener("click", ()=>{
    navigator.mediaDevices
            .getUserMedia({video: true})
            .then(stream => {
                video.srcObject = stream;
                video.play()
            })
})

audio_button.addEventListener("click", ()=>{
    navigator.mediaDevices
            .getUserMedia({audio: true})
            .then(stream => {
                audio.srcObject = stream;
                audio.play()
            })
})
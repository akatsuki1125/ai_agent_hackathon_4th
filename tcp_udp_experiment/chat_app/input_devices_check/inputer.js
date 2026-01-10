(() => {
    console.log("hello")
    const width = 300
    let height = 0

    const streaming = false

    let video = null
    let canvas = null
    let photo = null
    let startbutton= null

    function startup(){
        video = document.getElementById("video")
        /** * @type {HTMLCanvasElement} */
        canvas = document.getElementById("canvas")
        photo = document.getElementById("photo")
        startbutton = document.getElementById("startbutton")

        navigator.mediaDevices
            .getUserMedia({video: true})
            .then((stream) => {
                video.srcObject = stream;
                video.play()
            })
            .catch((err) => {
                console.error(`An error occured ${err}`)
            });
                

        video.addEventListener(
            // この canplay とか，addEventListner の第一，第三引数がよくわからん
            // false は毎回固定でいいんだろうか？というか，false って小文字なの？どうでもいいが
            // いいね，なんかこればっかやってたら相当賢くなれそうな気がするぞ？
            "canplay",
            (ev) => {
                if(!streaming){
                    height = (video.videoHeight / video.videoWidth) * width;

                    if (isNaN(height)){
                        height = width * 3 / 4
                    }
                    
                    video.setAttribute("width", width)
                    video.setAttribute("height", height)
                    canvas.setAttribute("width", width)
                    canvas.setAttribute("height", height)
                    streaming = true
                }
            },
            false,
        )

        startbutton.addEventListener(
            "click",
            (ev) => {
                takepicture();
                ev.preventDefault();
            },
            false,
        )

        clearPhoto();
    }

    function clearPhoto(){
        /** * @type {CanvasRenderingContext2D} */
        const context = canvas.getContext("2d");
        context.fillStyle = "#AAA";
        context.fillRect(0, 0, canvas.width, canvas.height);

        const data = canvas.toDataURL("image/png");
        photo.setAttribute("src", data);
    }

    function takepicture(){
        /** * @type {CanvasRenderingContext2D} */
        const context = canvas.getContext("2d");
        if (width && height){
            canvas.width = width
            canvas.height = height
            context.drawImage(video, 0, 0, width, height)

            const data = canvas.toDataURL("image/png")
            photo.setAttribute("src", data);
        }else{
            clearPhoto()
        }
    }

    window.addEventListener("load", startup, false)
})()
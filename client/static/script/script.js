const loadGradientScript = () => {
    let script = document.createElement("script");
    script.src = "https://cdn.jsdelivr.net/gh/greentfrapp/pocoloco@minigl/minigl.js";
    script.onload = () => {
        var gradient = new Gradient();
        gradient.initGradient("#canvas");
    };
    document.head.appendChild(script);
};

const resizeCanvas = () => {
    let canvas = document.getElementById("canvas");
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
};

window.onload = () => {
    loadGradientScript();
    resizeCanvas();
};

window.onresize = () => {
    resizeCanvas();
};

document.addEventListener("DOMContentLoaded", function(){
    //console.log("Page loaded.");
    //console.log(document.body.innerHTML);
    const button = document.getElementById("ID_generator");
    if (button) {
        //console.log("Button found!");
        button.addEventListener("click", async function () {
            //console.log("Button clicked!");
            try {
                let response = await fetch("/generate_new_id");
                let data = await response.json();
                //console.log(data); 
                document.getElementById("ID_value").innerText = data.lobby_id;
            } catch (error) {
                console.error("Error:", error);
            }
        });
    } else {
        //console.error("No button found.");
    }
});
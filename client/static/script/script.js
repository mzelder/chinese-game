function idGeneration(){
    let id = '';
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    const length = 10;
    for (let i=0; i<length; i++) {
        id += characters.charAt(Math.floor(Math.random() * characters.length));
    }
    document.getElementById('uniqueId').textContent = "Your lobby's ID:" + id;
};

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

setInterval(function () {
    let colors = ["#e9572f", "#1f7b8f", "#cf3881", "#5248b5"]; // array of colors to choose from
    let randomColor = colors[Math.floor(Math.random() * colors.length)]; // choose a random color
    document.getElementById("change-color").style.color = randomColor; // set the background color of the div to the chosen color
}, 1000); // run the function every 5 seconds (5000 milliseconds)
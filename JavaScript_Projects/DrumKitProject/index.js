var numOfButtons = document.querySelectorAll("button").length;
for (let i = 0; i < numOfButtons; i++){
    document.querySelectorAll("button")[i].addEventListener("click", handleClick);
}
addEventListener("keydown", handleKeyPress());

function handleClick() {
    var buttonInnerHTML = this.innerHTML;
    switch (buttonInnerHTML) {
        case "w":
            playSound("tom-1.mp3");
            break;
        case "a":
            playSound("tom-2.mp3");
            break;
        case "s":
            playSound("tom-3.mp3");
            break;
        case "d":
            playSound("tom-4.mp3");
            break;
        case "j":
            playSound("snare.mp3");
            break;
        case "k":
            playSound("kick-bass.mp3");
            break;
        case "l":
            playSound("crash.mp3");
            break;
        default:
            console.log("Invalid button");


    }
}
function playSound(soundFilePath){
    var soundEffect = new Audio("sounds/"+soundFilePath);
    soundEffect.play();
}

function handleKeyPress(event) {
    switch (event.key) {
        case "w":
            playSound("tom-1.mp3");
            break;
        case "a":
            playSound("tom-2.mp3");
            break;
        case "s":
            playSound("tom-3.mp3");
            break;
        case "d":
            playSound("tom-4.mp3");
            break;
        case "j":
            playSound("snare.mp3");
            break;
        case "k":
            playSound("kick-bass.mp3");
            break;
        case "l":
            playSound("crash.mp3");
            break;
        default:
            console.log("Invalid button");
    }         
}
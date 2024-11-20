var randomNumber1 = Math.floor(Math.random() * 6) + 1;
var randomNumber2 = Math.floor(Math.random() * 6) + 1;

document.getElementById("p1dice").src = "images/dice" + randomNumber1 + ".png";
document.getElementById("p2dice").src = "images/dice" + randomNumber2 + ".png";
if (randomNumber1 > randomNumber2) {
  document.getElementById("title").innerHTML = "Player 1 wins!";
}
else if (randomNumber2 > randomNumber1) {
  document.getElementById("title").innerHTML = "Player 2 wins!";
}
else {
  document.getElementById("title").innerHTML = "It's a tie!";
  }
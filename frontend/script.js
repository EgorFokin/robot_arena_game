

var players;

function draw_players(ctx){
    if (!players)return;
    console.log(players);
    for (let player of players){
        console.log(player.position.x,player.position.y);
        ctx.fillStyle = 'red';
        const radius = 50;
        ctx.arc(player.position.x, player.position.y, radius, 0, 2 * Math.PI, false);
        ctx.fill();

        ctx.fillStyle = 'black';
        ctx.font = "15px Arial";
        ctx.textAlign = "center";
        ctx.fillText(player.name, player.position.x, player.position.y+65); 


        ctx.fillStyle = 'red';
        ctx.fillRect(player.position.x-50, player.position.y+70, 100, 10);
        ctx.fillStyle = 'green';
        ctx.fillRect(player.position.x-50, player.position.y+70, player.health, 10);
    }
}

function game_loop(){
    const canvas = document.querySelector("#game-canvas");
    const ctx = canvas.getContext('2d');
    ctx.canvas.width  = window.innerWidth;
    ctx.canvas.height = window.innerHeight;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    draw_players(ctx);
    window.requestAnimationFrame(game_loop);
}

window.addEventListener("DOMContentLoaded", () => {
    // Initialize the UI.
    const canvas = document.querySelector("#game-canvas");
    const websocket = new WebSocket("ws://localhost:8765/");

    websocket.addEventListener("message", ({ data }) => {
        players = JSON.parse(data);
      });
    

  });

game_loop();
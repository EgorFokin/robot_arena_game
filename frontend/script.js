var players;
var player_sprites={"body":{}, "head":{}, "bracelet":{}, "pendant":{}, "weapon":{}};
var weapon_frames={};
var background_img = new Image();
var weapon_speed = 0.03;
var weapon_angle = 90;
var dmg_dealt;

function get_closest_player(player){
    let closest_player = null;
    for (let p of players){
        if (p.name == player.name)continue;
        if (p.team == player.team)continue;
        if (!closest_player)closest_player = p;
        if (Math.hypot(player.position.x-p.position.x, player.position.y-p.position.y) < Math.hypot(player.position.x-closest_player.position.x, player.position.y-closest_player.position.y)){
            closest_player = p;
        }
    }
    return closest_player
}


function draw_player_body(ctx, player){

    ctx.save();
    ctx.translate(player.position.x, player.position.y);
    let closest_player = get_closest_player(player);
    if (closest_player.position.x<player.position.x)ctx.scale(-1, 1);
    else ctx.scale(1, 1);

    ctx.drawImage(player_sprites.body[player.appearance.body], -50, -50, 100, 100);
    ctx.drawImage(player_sprites.head[player.appearance.head], -50, -50, 100, 100);
    ctx.drawImage(player_sprites.bracelet[player.appearance.bracelet], -50, -50, 100, 100);
    ctx.drawImage(player_sprites.pendant[player.appearance.pendant], -50, -50, 100, 100);

    ctx.restore();
}

function draw_weapon(ctx, player){
    ctx.save();
    ctx.translate(player.position.x-10, player.position.y+50);
    let closest_player = get_closest_player(player);
    if (closest_player.position.x<player.position.x)ctx.scale(-1, 1);
    else ctx.scale(1, 1);
    if (Math.hypot(player.position.x-closest_player.position.x, player.position.y-closest_player.position.y)<150){
        if (!weapon_frames[player.name] || weapon_frames[player.name]==Math.floor(1/weapon_speed))weapon_frames[player.name] = 0;
        ctx.rotate(weapon_frames[player.name]/Math.floor(1/weapon_speed)*weapon_angle*(Math.PI/180));
        weapon_frames[player.name]++;
    }
    
    ctx.drawImage(player_sprites.weapon[player.appearance.weapon],0, -100-10, 100, 100);
    ctx.restore();
}

function draw(ctx){
    ctx.drawImage(background_img, 0, 0, ctx.canvas.width, ctx.canvas.height);
    
    if (!players)return;
    for (let player of players){
        draw_player_body(ctx, player);
        draw_weapon(ctx, player);


        ctx.fillStyle = player.team;
        ctx.font = "bold 15px Courier New";
        ctx.textAlign = "center";
        ctx.fillText(player.name, player.position.x, player.position.y+65); 

        ctx.fillStyle = 'red';
        ctx.fillRect(player.position.x-50, player.position.y+70, 100, 5);
        ctx.fillStyle = 'green';
        ctx.fillRect(player.position.x-50, player.position.y+70, player.health, 5);


    }
}

function load_sprites(){
    
    for (let player of players){
        if (!player_sprites.body[player.appearance.body]){
            player_sprites.body[player.appearance.body]=new Image();
            player_sprites.body[player.appearance.body].src = "assets/Body/"+player.appearance.body+".png";
        }
        if (!player_sprites.head[player.appearance.head]){
            player_sprites.head[player.appearance.head]=new Image();
            player_sprites.head[player.appearance.head].src = "assets/Head/"+player.appearance.head+".png";
        }
        if (!player_sprites.bracelet[player.appearance.bracelet]){
            player_sprites.bracelet[player.appearance.bracelet]=new Image();
            player_sprites.bracelet[player.appearance.bracelet].src = "assets/Bracelet/"+player.appearance.bracelet+".png";
        }
        if (!player_sprites.pendant[player.appearance.pendant]){
            player_sprites.pendant[player.appearance.pendant]=new Image();
            player_sprites.pendant[player.appearance.pendant].src = "assets/Pendant/"+player.appearance.pendant+".png";
        }
        if (!player_sprites.weapon[player.appearance.weapon]){
            player_sprites.weapon[player.appearance.weapon]=new Image();
            player_sprites.weapon[player.appearance.weapon].src = "assets/Weapon/"+player.appearance.weapon+".png";
        }

    }
}

function game_loop(){
    const canvas = document.querySelector("#game-canvas");
    const ctx = canvas.getContext('2d');
    ctx.canvas.width  = window.innerWidth;
    ctx.canvas.height = window.innerHeight;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    draw(ctx);
    window.requestAnimationFrame(game_loop);
}

function on_button_pressed(event) {
    const data = {type:"button_press",content:event.currentTarget.action};
    event.currentTarget.websocket.send(JSON.stringify(data));
}

window.addEventListener("DOMContentLoaded", () => {
    // Initialize the UI.
    const canvas = document.querySelector("#game-canvas");
    const websocket = new WebSocket("ws://localhost:8765/");

    
    background_img.src = "assets/a844fb83-ba9b-4fc2-82b3-80d9890289cf.png";

    websocket.addEventListener("message", ({ data }) => {
        players = JSON.parse(data);
        load_sprites();
      });
    
    const start_btn = document.querySelector("#start-btn");
    start_btn.addEventListener("click", on_button_pressed);
    start_btn.websocket = websocket;
    start_btn.action = "start";

    const reset_btn = document.querySelector("#reset-btn");
    reset_btn.addEventListener("click", on_button_pressed);
    reset_btn.websocket = websocket;
    reset_btn.action = "reset";

  });

  

game_loop();
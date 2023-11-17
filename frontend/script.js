var state;
var players;
var boxes;
var coins = 10000;
var damage_events = [];
var player_sprites={"body":{}, "head":{}, "bracelet":{}, "pendant":{}, "weapon":{}};
var hit_sprite = new Image();
var weapon_frames={};
var box_img = new Image();
var weapon_speed = 0.03;
var weapon_angle = 90;
var dmg_dealt;
var prev_phase = null;
var canvas = null;

var current_bet = {
    "team":null,
    "amount":null
}

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

function draw_damage_events(ctx){
    ctx.save();
    if (!damage_events)return;
    for (let damage_event of damage_events){
        ctx.fillStyle = 'red';
        ctx.font = `bold ${10+Math.floor(damage_event.dmg/2)}px Courier New` ;
        ctx.textAlign = "center";
        ctx.fillText(damage_event.dmg.toString()+(damage_event.dmg > 15 ? " Crit!" :""), damage_event.x, damage_event.y-damage_event.frame/2); 
        damage_event.frame+=1;
        if (damage_event.frame<50){
            ctx.drawImage(hit_sprite,200*(Math.floor(damage_event.frame/20)%5),200*Math.floor(damage_event.frame/25),200,200, damage_event.x-50, damage_event.y-50,100,100)
        }
        }
    for (let i=damage_events.length-1; i>=0; i--){
        if (damage_events[i].frame>100){
            damage_events.splice(i, 1);
        }
    }
    ctx.restore();
}

function draw_boxes(ctx){
    ctx.save();
    if (!boxes)return;
    for (let box of boxes){
        ctx.fillStyle = 'brown';
        ctx.drawImage(box_img,box.position.x-25, box.position.y-25, 50, 50);
    }
    ctx.restore();
}

function draw(ctx){
    draw_damage_events(ctx);
    draw_boxes(ctx);
    if (!players)return;
    for (let player of players){
        draw_player_body(ctx, player);
        draw_weapon(ctx, player);
        
        ctx.textAlign = "center";
        ctx.font = "bold 15px Courier New";
        ctx.strokeStyle = 'black'; 
        ctx.lineWidth = 5; 
        ctx.strokeText(player.name, player.position.x, player.position.y+65);
        ctx.fillStyle = player.team;
        ctx.fillText(player.name, player.position.x, player.position.y+65); 

        ctx.fillStyle = 'red';
        ctx.fillRect(player.position.x-50, player.position.y+70, 100, 5);
        ctx.fillStyle = 'green';
        ctx.fillRect(player.position.x-50, player.position.y+70, player.health, 5);
    }
    
}

function load_player_sprites(){
    
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

function get_coins_from_cookie(){
    let cookies = document.cookie.split(';');
    for (let cookie of cookies){
        if (cookie.split('=')[0].trim() == "coins"){
            coins = parseInt(cookie.split('=')[1]);
        }
    }
}

function change_coins_in_cookie(){
    document.cookie = `coins=${coins}; expires=Fri, 31 Dec 9999 23:59:59 GMT;SameSite=Strict;`;
    
}

function game_loop(){
    const ctx = canvas.getContext('2d');
    get_coins_from_cookie();
    document.querySelector("#coins_number").innerHTML = coins;
    ctx.canvas.width  = window.innerWidth;
    ctx.canvas.height = window.innerWidth/1536*703;
    ctx.scale(window.innerWidth/1536,window.innerWidth/1536);
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    if (state){
        if (state.phase == "game_active"){
            draw(ctx);
            document.querySelector("main").style.display = "none";
            if (state.phase == "game_active" && prev_phase == "betting"){
                if (current_bet.team)
                document.querySelector("#current_bet_match").innerHTML = `Current bet: ${current_bet.amount} on <span style="color: ${current_bet.team};">${current_bet.team}</span>`;
            }
            
        }
        if (state.phase == "betting"){
            let timer = 30 - Math.floor((Date.now() - new Date(state.betting_start_timestamp*1000))/1000);
            document.querySelector("#next_match_timer p").innerHTML = `${timer} seconds!`;

            if (timer<=20)document.querySelector("#notification").style.display = "none";

            document.querySelector("main").style.display = "block";
            if (prev_phase == "game_active"){
                if (state.previous_winner == current_bet.team){
                    coins+=current_bet.amount*4;
                    document.querySelector("#notification").style.display = "block";
                    document.querySelector("#notification").style.backgroundColor = "rgba(0,255,0,0.5)";
                    document.querySelector("#notification").innerHTML = `<span style="color: ${state.previous_winner};">${state.previous_winner}</span> team won! You won ${current_bet.amount*3} coins!`;
                }
                else{
                    if (current_bet.team)coins-=current_bet.amount;
                    document.querySelector("#notification").style.display = "block";
                    document.querySelector("#notification").style.backgroundColor = (current_bet.amount!=null?"rgba(255,0,0,0.5)":"rgba(150,150,150,0.5)");
                    document.querySelector("#notification").innerHTML = `<span style="color: ${state.previous_winner};">${state.previous_winner}</span> team won!`+ (current_bet.amount!=null?` You lost ${current_bet.amount} coins!`:"");
                    if (coins<=0){
                        document.querySelector("#notification").innerHTML = `<span style="color: ${state.previous_winner};">${state.previous_winner}</span> team won! You have lost all of your coins! But you found 500 coins on the street!`;
                        coins = 500;
                    }
                }
                
                current_bet = {
                    "team":null,
                    "amount":null}
                
                document.querySelector("#current_bet_match").innerHTML = "";
                document.querySelectorAll(".team_bet").forEach((element) => element.style.display = "none");
            }
        }
        prev_phase = state.phase;
    } 
    change_coins_in_cookie();
    window.requestAnimationFrame(game_loop);
}

function bet_button_pressed(event){
    team = event.getAttribute("id").split('_')[0];
    if (current_bet.team == team || coins==0)return;

    current_bet.amount = Math.min(1000,coins);
    current_bet.team = team;

    document.querySelectorAll(".team_bet").forEach((element) => element.style.display = "none");
    document.querySelector(`#${team}_team_bet`).style.display = "block";
    document.querySelector(`#${current_bet.team}_team_bet_amount`).innerHTML = `${current_bet.amount} coins`;
}

function increase_bet(){
    if (current_bet.amount*2>coins)return;
    current_bet.amount*=2;
    document.querySelector(`#${current_bet.team}_team_bet_amount`).innerHTML = `${current_bet.amount} coins`;
}

function decrease_bet(){
    current_bet.amount/=2;
    if (current_bet.amount<Math.min(1000,coins)){
        document.querySelector(`#${current_bet.team}_team_bet`).style.display = "none";
        current_bet.team = null;
        
    }
    document.querySelector(`#${current_bet.team}_team_bet_amount`).innerHTML = `${current_bet.amount} coins`;
}

window.addEventListener("DOMContentLoaded", () => {
    // Initialize the UI.
    canvas = document.querySelector("#game-canvas");
    const websocket = new WebSocket("ws://192.168.1.67:8765/");


    hit_sprite.src = "assets/hit_animation.png";
    box_img.src = "assets/box.png";

    document.querySelector("#coins_number").innerHTML = coins - current_bet.amount;

    websocket.addEventListener("message", ({ data }) => {
        state = JSON.parse(data);
        players = []
        boxes = []
        for (let object of state.active_objects){
            if (object.type == "player")players.push(object);
            if (object.type=="box")boxes.push(object);
        }
        for (let damage_event of state.damage_events){
            damage_events.push({x:damage_event.x, y:damage_event.y, dmg:damage_event.damage, frame:0});
            
        }
        load_player_sprites();
      });

      game_loop();
  });

  


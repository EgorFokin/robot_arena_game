import json
from datetime import timedelta,datetime
import random
from vectors import Vector
import time

prev_update_datetime = None
game_active = False

players = []


GRAVITY = 100
PLAYER_NUM = 20

impulse_cooldown = 0

def remove_dead_players():
    #removes players with health <=0 from the players list
    global players
    for player in players:
        if player["health"]<=0:
            players.remove(player)

def check_for_border_collisions():
    #checks if a player is colliding with the border and if so, changes the velocity accordingly
    global players
    for player in players:
        if (player["position"].y>665):
             player["position"].y = 665
             player["velocity"].y = -player["velocity"].y*0.7
        if (player["position"].y<50):
             player["position"].y = 50
             player["velocity"].y = -player["velocity"].y*0.7
        if (player["position"].x<50):
             player["position"].x = 50
             player["velocity"].x = -player["velocity"].x*0.7
        if (player["position"].x>1300):
             player["position"].x = 1300
             player["velocity"].x = -player["velocity"].x*0.7
    
def apply_velocity(td):
    #applies the velocity of each player to its position 
    global players
    for player in players:
        player["position"] += player["velocity"]*td

def apply_gravity(td):
    #applies gravity to each player
    global players
    for player in players:
        player["velocity"] += Vector(0,GRAVITY)*td

def apply_random_impulses():
    #applies a random impulse to random players
    global players
    impulse_players = random.sample(players,random.randint(1,len(players)//2))
    for player in impulse_players:
        player["velocity"]+=Vector(random.randint(-1000,1000),random.randint(-1000,1000))
         

def calculate_collisions():
     #calculates collisions between players and changes their velocity and health accordingly
     global players
     for i in range(len(players)):
        for j in range(i+1,len(players)):
             if  (players[j]["position"]-players[i]["position"]).mag()<100:
                  
                  direction = (players[i]["position"]-players[j]["position"]).norm()
                  collision_v = (players[i]["velocity"].proj(direction).mag() +players[j]["velocity"].proj(direction).mag())*direction/2
                  players[i]["velocity"]-=players[i]["velocity"].proj(direction)
                  players[i]["velocity"]+=collision_v
                  players[j]["velocity"]-=players[j]["velocity"].proj(direction)
                  players[j]["velocity"]-=collision_v
                  players[i]["health"]-=0.01

def populate_players():
    #populates the players list with random players
    global players
    players = []
    for i in range(PLAYER_NUM):
        players.append({"name":"player"+str(i),"position":Vector(random.randint(50,1300),random.randint(50,600)),"velocity":Vector(0,0),"health":100})

def update():
    global prev_update_datetime,players,impulse_cooldown
    td = (datetime.now() - prev_update_datetime).total_seconds()
    impulse_cooldown-=td
    if impulse_cooldown<0:
         apply_random_impulses()
         impulse_cooldown = random.uniform(0.5,2)
    prev_update_datetime = datetime.now()
    calculate_collisions()
    apply_gravity(td)
    check_for_border_collisions()
    apply_velocity(td)
    remove_dead_players()
    time.sleep(1/1000)

def start_game():
    global prev_update_datetime,players
    prev_update_datetime = datetime.now()
    populate_players()
    while(True):
            if (game_active):
                update()

def pause():
     global game_active
     game_active = False

def unpause():
     global prev_update_datetime,game_active
     game_active = True
     prev_update_datetime = datetime.now()

def reset():
     global game_active
     game_active = False
     populate_players()


def get_state():
     state = {"players":[]}
     for player in players:
          state["players"].append({"name":player["name"],
                                  "position":{"x":player["position"].x,"y":player["position"].y},
                                  "health":player["health"]})
     return state
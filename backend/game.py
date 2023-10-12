import json
from datetime import timedelta,datetime
from vectors import Vector
import time

prev_update_datetime = None
game_active = False

players = [{"name": "player1","position": Vector(50,100),"health": 50,"velocity":Vector(0,0)},
           {"name": "player2","position": Vector(70,250),"health": 100,"velocity":Vector(0,0)},
           {"name": "player3","position": Vector(90,400),"health": 0,"velocity":Vector(0,0)}]


GRAVITY = 100

def update():
    global prev_update_datetime,players
    td = (datetime.now() - prev_update_datetime).total_seconds()
    prev_update_datetime = datetime.now()
    for player in players:
        for player2 in players:
             if player2 != player and (player2["position"]-player["position"]).mag()<100:
                  direction = (player["position"]-player2["position"]).norm()
                  collision_v = (player["velocity"].proj(direction) +player2["velocity"].proj(direction)).mag()*direction#*100
                  player["velocity"]+=collision_v

        player["velocity"] += Vector(0,GRAVITY)*td
        if (player["position"].y>665):
             player["position"].y = 665
             player["velocity"].y = -abs(player["velocity"].y)*0.7
        if (player["position"].y<0):
             player["position"].y = 665
             player["velocity"].y = -abs(player["velocity"].y)*0.7
        if (player["position"].x<0):
             player["position"].x = 0
             player["velocity"].x = -abs(player["velocity"].x)*0.7
        if (player["position"].x>1300):
             player["position"].x = 1300
             player["velocity"].x = -abs(player["velocity"].x)*0.7
        player["position"] += player["velocity"]*td
    #time.sleep(1/1000)

def start_game():
    global prev_update_datetime
    prev_update_datetime = datetime.now()
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
     y = 100
     for player in players:
           player["position"] = Vector(50,y)
           player["velocity"]:Vector(0,0)
           y+=150


def get_state():
     state = {"players":[]}
     for player in players:
          state["players"].append({"name":player["name"],
                                  "position":{"x":player["position"].x,"y":player["position"].y},
                                  "health":player["health"]})
     return state
import json
from datetime import timedelta,datetime

prev_update_datetime = None

players = [{"name": "player1","position": {"x": 50,"y": 100},"health": 50},
           {"name": "player2","position": {"x": 50,"y":250},"health": 100},
           {"name": "player3","position": {"x": 50,"y": 400},"health": 0}]


def update():
    global prev_update_datetime,players
    td = (datetime.now() - prev_update_datetime).total_seconds()
    prev_update_datetime = datetime.now()
    for player in players:
        player["position"]["x"] += 10*td
        player["health"] += 10*td

def start_game():
    global prev_update_datetime
    prev_update_datetime = datetime.now()
    while(True):
            update()
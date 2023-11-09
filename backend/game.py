import json
from datetime import timedelta, datetime
import random
from vectors import Vector
import time
import math
from game_object import *

prev_update_datetime = None

active_objects = []

apperances = {
    "bracelet": ["Broken Rolex", "Golden Cartier", "Rolex Watch", "Rope"],
    "head": ["Bone", "Crystal", "Defense", "Fiend", "Intellect", "Samurai", "Teleport", "Titan"],
    "pendant": ["Dollar sign", "Golden Chain", "Golden Sol", "Silver Lock"],
    "weapon": ["Baseball Bat", "Claws", "Katana", "Knife", "Knuckles", "Nunchaku", "Sai", "Sword"]}

team_count = 2
teams = ["red", "blue", "green", "yellow"]
teams = teams[:team_count]

damage_events = []


GRAVITY = 200
PLAYER_NUM = 10
BOX_NUM = 20
DAMAGE_LOW = 1
DAMAGE_HIGH = 10

impulse_cooldown = 0
grace_period = 3

phase = "betting"

betting_start_time = datetime.now()

winner = None


def remove_dead_players():
    # removes players with health <=0 from the players list
    global active_objects
    for object in active_objects:
        if type(object) == Player and object.health <= 0:
            active_objects.remove(object)


def check_for_border_collisions():
    # checks if a player is colliding with the border and if so, changes the velocity accordingly
    global active_objects
    for object in active_objects:
        if (object.position.y+object.collision_radius > 615):
            object.position.y = 615 - object.collision_radius
            if type(object) == Box:
                object.velocity.y = -object.velocity.y*0.2
            else:
                object.velocity.y = -object.velocity.y*0.7
        if (object.position.y-object.collision_radius < 0):
            object.position.y = object.collision_radius
            if type(object) == Box:
                object.velocity.y = -object.velocity.y*0.2
            else:
                object.velocity.y = -object.velocity.y*0.7
        if (object.position.x-object.collision_radius < 0):
            object.position.x = object.collision_radius
            if type(object) == Box:
                object.velocity.x = -object.velocity.x*0.2
            else:
                object.velocity.x = -object.velocity.x*0.7
        if (object.position.x+object.collision_radius > 1500):
            object.position.x = 1500 - object.collision_radius
            if type(object) == Box:
                object.velocity.x = -object.velocity.x*0.2
            else:
                object.velocity.x = -object.velocity.x*0.7


def apply_velocity(td):
    # applies the velocity of each player to its position
    global active_objects
    for object in active_objects:
        object.position += object.velocity*td
        if type(object) == Box and object.position.y-object.collision_radius > 300:
            object.velocity.x -= object.velocity.x*td*2


def apply_gravity(td):
    # applies gravity to each player
    global active_objects
    for object in active_objects:
        object.velocity += Vector(0, GRAVITY)*td


def apply_random_impulses():
    # applies a random impulse to random players
    global active_objects
    players = [object for object in active_objects if type(object) == Player]
    impulse_players = random.sample(
        players, random.randint(1, math.ceil(len(players)/2)))
    for player in impulse_players:
        target = random.choice(players)
        while target.team == player.team:
            target = random.choice(players)
        player.velocity += (target.position-player.position)*0.7


def calculate_collisions():
    # calculates collisions between active_objects and changes their velocity and health accordingly
    global active_objects
    for i in range(len(active_objects)):
        for j in range(i+1, len(active_objects)):
            offset = active_objects[i].collision_radius + \
                active_objects[j].collision_radius
            if type(active_objects[i]) == Player and type(active_objects[j]) == Player and \
                    (active_objects[j].position-active_objects[i].position).mag() < offset:
                direction = (active_objects[i].position -
                             active_objects[j].position).norm()
                collision_v = (active_objects[i].velocity.proj(direction).mag(
                ) + active_objects[j].velocity.proj(direction).mag())*direction/2

                active_objects[i].velocity += collision_v - active_objects[i].velocity.proj(
                    direction)
                active_objects[j].velocity += Vector(0, 0)-collision_v - active_objects[j].velocity.proj(
                    direction)

                if active_objects[i].team != active_objects[j].team:
                    if (grace_period <= 0):
                        damage = random.uniform(DAMAGE_LOW, DAMAGE_HIGH)
                        if random.randint(0, 1):
                            active_objects[i].health -= damage
                        else:
                            active_objects[j].health -= damage
                        center = (active_objects[i].position +
                                  active_objects[j].position)/2
                        damage_events.append(
                            {"x": center.x, "y": center.y, "damage": "{:.2f}".format(damage)})

            if type(active_objects[i]) == Box and type(active_objects[j]) == Box and\
                    abs(active_objects[i].position.x - active_objects[j].position.x) < offset and\
                    abs(active_objects[i].position.y - active_objects[j].position.y) < offset:

                if abs(active_objects[i].position.y - active_objects[j].position.y) > abs(active_objects[i].position.x - active_objects[j].position.x):
                    collision_v = (
                        (active_objects[i].velocity.y)+(active_objects[j].velocity.y)) * 0.5
                    if active_objects[i].position.y < active_objects[j].position.y:
                        active_objects[i].position.y = active_objects[j].position.y - offset
                    else:
                        active_objects[j].position.y = active_objects[i].position.y - offset
                    active_objects[i].velocity.y = collision_v
                    active_objects[j].velocity.y = collision_v
                else:
                    collision_v = (
                        (active_objects[i].velocity.x)+(active_objects[j].velocity.x)) * 0.5
                    if active_objects[i].position.x < active_objects[j].position.x:
                        active_objects[i].position.x = active_objects[j].position.x - offset
                    else:
                        active_objects[j].position.x = active_objects[i].position.x - offset
                    active_objects[i].velocity.x = collision_v
                    active_objects[j].velocity.x = collision_v

            if set([type(active_objects[i]), type(active_objects[j])]) == set([Box, Player]):
                if type(active_objects[i]) == Box and type(active_objects[j]) == Player:
                    obj_box = active_objects[i]
                    obj_player = active_objects[j]
                else:
                    obj_box = active_objects[j]
                    obj_player = active_objects[i]
                if (obj_box.calculate_col_point(obj_player)-obj_player.position).mag() < obj_player.collision_radius:
                    direction = (obj_box.position -
                                 obj_player.position).norm()
                    collision_v = (obj_box.velocity.proj(direction).mag(
                    ) + obj_player.velocity.proj(direction).mag())*direction/2

                    obj_box.velocity += (collision_v - obj_box.velocity.proj(
                        direction))
                    obj_player.velocity += Vector(0, 0) - collision_v - obj_player.velocity.proj(
                        direction)


def populate_players():
    # populates the players list with random players
    global active_objects
    for i in range(PLAYER_NUM):
        team_index = random.randint(0, len(teams)-1)
        team_color = teams[team_index]
        head = random.choice(apperances["head"])
        active_objects.append(Player("player"+str(i),
                              Vector(random.randint(50, (1500//len(teams))) + (1500//len(teams)) * (team_index),
                              random.randint(50, 550)),
                              Vector(0, 0),
                              100,
                              {"head": head, "body": head + "_body", "pendant": random.choice(apperances["pendant"]),
                              "bracelet": random.choice(apperances["bracelet"]), "weapon": random.choice(apperances["weapon"])}, team_color))


def spawn_boxes():
    # spawns boxes at random locations
    global active_objects
    for i in range(7):
        for j in range(2):
            active_objects.append(Box(Vector(750 + j*40, 615 - i*40),
                                      Vector(0, 0)))


def update():

    global prev_update_datetime, impulse_cooldown, grace_period, active_objects, phase, winner
    td = (datetime.now() - prev_update_datetime).total_seconds()
    impulse_cooldown -= td
    if (grace_period > 0):
        grace_period -= td
    if impulse_cooldown < 0:
        apply_random_impulses()
        impulse_cooldown = random.uniform(0.5, 2)
    prev_update_datetime = datetime.now()
    calculate_collisions()
    apply_gravity(td)
    check_for_border_collisions()
    apply_velocity(td)
    remove_dead_players()
    if len(set([object.team for object in active_objects if type(object) == Player])) == 1:
        winner = [object.team for object in active_objects if type(
            object) == Player][0]
        end_game()
        phase = "betting"
    time.sleep(1/1000)


def end_game():
    global phase, betting_start_time
    phase = "betting"
    betting_start_time = datetime.now()


def start_game():
    global prev_update_datetime, phase
    prev_update_datetime = datetime.now()
    reset()
    while (True):
        if (phase == "game_active"):
            update()
        elif (phase == "betting"):
            if (datetime.now() - betting_start_time > timedelta(seconds=30)):
                reset()
                phase = "game_active"


def reset():
    global active_objects, prev_update_datetime
    active_objects = []
    populate_players()
    spawn_boxes()
    prev_update_datetime = datetime.now()


def get_state():
    state = {"active_objects": [],
             "damage_events": damage_events[:], "phase": phase, "betting_start_timestamp": datetime.timestamp(betting_start_time), "previous_winner": winner}
    damage_events.clear()
    for object in active_objects:
        state["active_objects"].append(object.to_dict())
    return state

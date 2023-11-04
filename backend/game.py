import json
from datetime import timedelta, datetime
import random
from vectors import Vector
import time
import math
from game_object import *

prev_update_datetime = None
game_active = False

active_objects = []

apperances = {
    "bracelet": ["Broken Rolex", "Golden Cartier", "Rolex Watch", "Rope"],
    "head": ["Bone", "Crystal", "Defense", "Fiend", "Intellect", "Samurai", "Teleport", "Titan"],
    "pendant": ["Dollar sign", "Golden Chain", "Golden Sol", "Silver Lock"],
    "weapon": ["Baseball Bat", "Claws", "Katana", "Knife", "Knuckles", "Nunchaku", "Sai", "Sword"]}

team_count = 4
teams = ["red", "blue", "green", "yellow"]
teams = teams[:team_count]

damage_events = []


GRAVITY = 200
PLAYER_NUM = 10

impulse_cooldown = 0
grace_period = 3


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
        if type(object) == Box and object.position.x-object.collision_radius < 50:
            object.velocity.x -= object.velocity.x*td*0.5


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
            if (active_objects[j].position-active_objects[i].position).mag() < active_objects[i].collision_radius + active_objects[j].collision_radius:

                direction = (active_objects[i].position -
                             active_objects[j].position).norm()
                collision_v = (active_objects[i].velocity.proj(direction).mag(
                ) + active_objects[j].velocity.proj(direction).mag())*direction/2

                if type(active_objects[i]) == Box:
                    active_objects[i].velocity += (collision_v - active_objects[i].velocity.proj(
                        direction))*0.5
                else:
                    active_objects[i].velocity += collision_v - active_objects[i].velocity.proj(
                        direction)
                if type(active_objects[j]) == Box:
                    active_objects[j].velocity += (Vector(0, 0)-collision_v - active_objects[j].velocity.proj(
                        direction))*0.5
                else:
                    active_objects[j].velocity += Vector(0, 0)-collision_v - active_objects[j].velocity.proj(
                        direction)

                if type(active_objects[i]) == Player and type(active_objects[j]) == Player and active_objects[i].team != active_objects[j].team:
                    if (grace_period <= 0):
                        damage = random.uniform(1, 10)
                        if random.randint(0, 1):
                            active_objects[i].health -= damage
                        else:
                            active_objects[j].health -= damage
                        center = (active_objects[i].position +
                                  active_objects[j].position)/2
                        damage_events.append(
                            {"x": center.x, "y": center.y, "damage": "{:.2f}".format(damage)})


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
    for i in range(10):
        active_objects.append(Box(Vector(random.randint(600, 900),
                                         random.randint(50, 550)),
                                  Vector(0, 0)))


def update():

    global prev_update_datetime, impulse_cooldown, grace_period, active_objects
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
        reset()
    time.sleep(1/1000)


def start_game():
    global prev_update_datetime
    prev_update_datetime = datetime.now()
    reset()
    while (True):
        if (game_active):
            update()


def pause():
    global game_active
    game_active = False


def unpause():
    global prev_update_datetime, game_active, grace_period
    grace_period = 3
    prev_update_datetime = datetime.now()
    game_active = True


def reset():
    global game_active, active_objects
    game_active = False
    active_objects = []
    populate_players()
    spawn_boxes()


def get_state():
    state = {"active_objects": [], "damage_events": damage_events[:]}
    damage_events.clear()
    for object in active_objects:
        state["active_objects"].append(object.to_dict())
    return state

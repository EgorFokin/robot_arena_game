from vectors import Vector


class GameObject():
    def __init__(self, position, velocity) -> None:
        self.position = position
        self.velocity = velocity
        self.collision_radius = None


class Player(GameObject):
    def __init__(self, name, position, velocity, health, appearance, team) -> None:
        super().__init__(position, velocity)
        self.name = name
        self.health = health
        self.appearance = appearance
        self.team = team
        self.collision_radius = 35

    def to_dict(self):
        return {"type": "player",
                "name": self.name,
                "position": {"x": self.position.x, "y": self.position.y},
                "health": self.health,
                "appearance": self.appearance,
                "team": self.team}



class Box(GameObject):
    def __init__(self, position, velocity) -> None:
        super().__init__(position, velocity)
        self.collision_radius = 20

    def to_dict(self):
        return {"type": "box",
                "position": {"x": self.position.x, "y": self.position.y}}
    
    def calculate_col_point(self, gameObject):
        if gameObject.position.x >= self.position.x + self.collision_radius:
            if gameObject.position.y <= self.position.y - self.collision_radius: return Vector(self.position.x + self.collision_radius, self.position.y - self.collision_radius)
            if gameObject.position.y < self.position.y + self.collision_radius: return Vector(self.position.x + self.collision_radius, gameObject.position.y)
            if gameObject.position.y >= self.position.y + self.collision_radius: return Vector(self.position.x + self.collision_radius, self.position.y + self.collision_radius)
        elif gameObject.position.x <= self.position.x - self.collision_radius:
            if gameObject.position.y <= self.position.y - self.collision_radius: return Vector(self.position.x - self.collision_radius, self.position.y - self.collision_radius)
            if gameObject.position.y < self.position.y + self.collision_radius: return Vector(self.position.x - self.collision_radius, gameObject.position.y)
            if gameObject.position.y >= self.position.y + self.collision_radius: return Vector(self.position.x - self.collision_radius, self.position.y + self.collision_radius)
        else:
            if gameObject.position.y <= self.position.y - self.collision_radius: return Vector(gameObject.position.x, self.position.y - self.collision_radius)
            else: return Vector(gameObject.position.x, self.position.y + self.collision_radius)
        


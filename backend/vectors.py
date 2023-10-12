import math

class Vector():
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __add__(self,b):
        return Vector(self.x + b.x, self.y + b.y)

    
    def __sub__(self, b):
        return Vector(self.x - b.x, self.y - b.y)

    def __mul__(self, b):
        return Vector(b * self.x, b * self.y)

    def __rmul__(self, b):
        return Vector(b * self.x, b * self.y)

    def __truediv__(self, b):
        if b != 0:
            return Vector(self.x / b, self.y / b)
        else:
            return Vector(self.x / 0.001, self.y / 0.001)

    def mag(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)
    
    def norm(self):
        return self/self.mag()
    
    def dot(self,b):
        return self.x*b.x+self.y*b.y
    
    def proj(self,b):
        return self.dot(b)/self.mag()**2*b

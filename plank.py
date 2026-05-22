from vpython import vec, box, color

class Plank:
    def __init__(self, start_pos, mass, length=2.0, thickness=0.2, width=5.0):
        self.mass = mass
        self.velocity = vec(0, 0, 0)
        self.net_force = vec(0, 0, 0) 
        self.model = box(   pos=start_pos, size=vec(length, thickness, width), color=color.blue)

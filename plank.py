from vpython import textures, vec, box, color

class Plank:
    def __init__(self, start_pos, mass, length=2.0, thickness=0.2, width=10.0):
        self.mass = mass
        self.velocity = vec(0, 0, 0)
        self.net_force = vec(0, 0, 0) 
        self.model = box(texture=textures.wood, outline=color.white, pos=start_pos, size=vec(length, thickness, width), color=vec(0.5, 0.25, 0), opacity=1)

import warnings
warnings.filterwarnings("ignore", message="pkg_resources is deprecated")

from vpython import canvas, rate, textures, vec, color, box

scene = canvas(width=800, height=600, background=color.black)
floor = box(pos=vec(0, -5, 0), size=vec(15, 0.1, 10), color=color.white, opacity=1)

class Plank:
    def __init__(self, start_pos, mass, length=2.0, thickness=0.2, width=10.0):
        self.mass = mass
        self.velocity = vec(0, 0, 0)
        self.net_force = vec(0, 0, 0) 
        self.model = box(texture=textures.wood, outline=color.white, pos=start_pos, size=vec(length, thickness, width), color=vec(0.5, 0.25, 0), opacity=1)

test_plank = Plank(start_pos=vec(10, 0, 0), mass=10)
test_plank = Plank(start_pos=vec(8, 0, 0), mass=10)
while True:
    rate(60) 
    pass


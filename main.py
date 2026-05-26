import warnings
warnings.filterwarnings("ignore", message="pkg_resources is deprecated")
from vpython import canvas, rate, vec, color, box, textures, arrow, points

scene = canvas()
scene.userzoom = False
scene.width = 1500
scene.background = color.white
scene.align ='right'
scene.resizable = False

plank_list = []

class Plank:
    def __init__(self, start_pos, mass, length=10.0, height = 2.0, width=50.0):
        self.mass = mass
        self.velocity = vec(0, 0, 0)
        self.net_force = vec(0, 0, 0)

        self.model = box(
            texture=textures.wood,
            pos=start_pos,
            size=vec(length, height, width),
            color=vec(0.5, 0.25, 0)
        )
        

box(pos=vec(0, 0, 0), radius=0.5,texture=textures.wood)

# visible axes
arrow(pos=vec(0, 0, 0), axis=vec(50, 0, 0), color=color.orange, shaftwidth=0.3)
arrow(pos=vec(0, 0, 0), axis=vec(0, 50, 0), color=color.cyan, shaftwidth=0.3)
arrow(pos=vec(0, 0, 0), axis=vec(0, 0, 50), color=color.white, shaftwidth=0.3)

# visible corners of area used
points(pos=[vec(50,50,50), vec(-50,50,50), vec(50,-50,50), vec(50,50,-50), vec(-50,-50,-50), vec(-50,-50,50), vec(50,-50,-50), vec(-50,50,-50)])

# walls
box(pos=vec(-50, -25, 0), length=0.1, height=50, width=100)
box(pos=vec(50, -25, 0), length=0.1, height=50, width=100)

p1 = Plank(start_pos=vec(0,0,0), mass=3.0)

plank_list.append(p1)

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


import warnings
warnings.filterwarnings("ignore", message="pkg_resources is deprecated")
from vpython import *

# Web VPython 3.2

#########################
# SCENE SETUP
#########################
scene.userzoom = False
scene.width = 1500
scene.background = color.white
scene.align ='right'
scene.resizable = False
scene.title = "<b>PHYSICS FINAL PROJECT: Spring Bridge</b>"

scene2 = canvas()
scene.select()
scene.visible = True
scene2.visible = True

#########################
# OBJ
#########################

plank_list = []

# replace Plank class with obj creation loop
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

class Spring:
    def __init__(self, k, plankL, plankR):
        self.k = k
        self.plank_A = plankL
        self.plank_B = plankR
        
        self.rest_length = mag(plankL.model.pos - plankR.model.pos)
        
        self.model = helix(
            pos=plankL.model.pos, 
            axis=(plankR.model.pos - plankL.model.pos), 
            radius=1.5, coils=8, thickness=0.3, color=color.gray(0.6)
        )

plank_list = []
spring_list = []

num_planks = 12
gap = 8.0 
start_x = -44

for i in range(num_planks):
    spawn_pos = vec(start_x + (i * gap), 0, 0)
    p = Plank(start_pos=spawn_pos, mass=5.0)
    
    if i == 0 or i == num_planks - 1:
        p.anchored = True
    else:
        p.anchored = False
        
    plank_list.append(p)

for i in range(num_planks - 1):
    s = Spring(k=200, plankL=plank_list[i], plankR=plank_list[i+1])
    spring_list.append(s)

# visible axes
arrow(pos=vec(0, 0, 0), axis=vec(50, 0, 0), color=color.orange, shaftwidth=0.3)
arrow(pos=vec(0, 0, 0), axis=vec(0, 50, 0), color=color.cyan, shaftwidth=0.3)
arrow(pos=vec(0, 0, 0), axis=vec(0, 0, 50), color=color.white, shaftwidth=0.3)

# visible corners of area used
corners = [vec(50,50,50), vec(-50,50,50), vec(50,-50,50), vec(50,50,-50), 
            vec(-50,-50,-50), vec(-50,-50,50), vec(50,-50,-50), vec(-50,50,-50)]
    

edges = [(0,1),(0,2),(0,3), (1,5),(1,7),(7,3), (4,5),(4,6),(4,7), (5,1),(5,2),(6,3), (2,6)]

for a,b in edges:
    curve(pos=[corners[a], corners[b]], color=color.black, radius=0.2)

# walls
box(pos=vec(-50, -25, 0), length=5, height=50, width=100, color=color.black)
box(pos=vec(50, -25, 0), length=5, height=50, width=100, color=color.black)

# floor
box(pos=vec(0, -50, 0), length=100, height=5, width=100, color=color.black)

#########################
# LIGHT SETUP
#########################

num_LL = 8
r_LL = 33
LLs = []

for i in range(num_LL):
    angle = 2*pi*i/num_LL
    LL = local_light(pos=vec(r_LL*cos(angle), 0, r_LL*sin(angle)), color=vec(random(), random(), random()))
    LLs.append(LL)
    
#scene = canvas(width=800, height=600, background=color.black)
#floor = box(pos=vec(0, -5, 0), size=vec(15, 0.1, 10), color=color.white, opacity=1)

#########################
# MAIN LOOP
#########################
t=0
while True: 
    rate(30)
    dt = 0.01 
    g = vec(0, -9.8, 0)

    for p in plank_list:
        if not p.anchored:
            p.net_force += p.mass * g 
            
            acceleration = p.net_force / p.mass
            p.velocity += acceleration * dt
            p.model.pos += p.velocity * dt      
        p.net_force = vec(0,0,0)
    print(plank_list[5].model.pos)

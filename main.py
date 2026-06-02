import warnings
warnings.filterwarnings("ignore", message="pkg_resources is deprecated")
from vpython import *

#Web VPython 3.2
    
#########################
# CONSTANTS
#########################
TORSION_TYPE = 0
TENSION_TYPE = 1
COMPRES = 2
STL_MAT = 0 # steel
ALM_MAT = 1 # aluminum
BRZ_MATERIAL = 2 # bronze

PLA_WIDTH = 10

WALL_WIDTH = 5

#########################
# INPUTS
#########################
PPL_NUM = 10
PPL_MASS = 5 # kg
PPL_SPEED = 10 # m/s

PLA_NUM = 12

K_SPR = 50 # N/m
NUM_SPR = 3 # N/m
SPR_TYPE = 0 # defaults to torsion type
SPR_MAT = 0 # defaults to aluminum

extra_visuals = True

#########################
# SCENE SETUP
#########################
scene.userzoom = False
scene.resizable = False
scene.width = 1000
scene.background = color.white
scene.title = "<b>PHYSICS FINAL PROJECT: Spring Bridge</b>"

scene2 = canvas()
scene.select()
scene.visible = True
scene2.visible = True

#########################
# WORLD
#########################

BRIDGE_LEN = PLA_WIDTH*PLA_NUM
WALL_L = box(pos=vec(-BRIDGE_LEN/2 -WALL_WIDTH*PPL_NUM, -25, 0), size=vec(WALL_WIDTH*2*PPL_NUM, 50+10, 100)) # people start from here
WALL_R = box(pos=vec(BRIDGE_LEN/2, -25, 0), size=vec(WALL_WIDTH, 50+10, 100)) # +10 is to fill edge due to floor's size.y
FLOOR = box(pos=vec(0, -50, 0), size=vec(BRIDGE_LEN, 10, 100))

#########################
# INIT PEOPLE
#########################

person_list = []

PPL_DIM = vec(5,10,5)
class Person:
    def __init__(self, start_pos, mass, vel):
        self.pos = start_pos
        self.mass = mass
        self.vel = vel
        
        self.model = box(
            texture = textures.wood,
            pos = self.pos,
            size = PPL_DIM,
            color = vec(0,0,0)
        )
        
for i in range(PPL_NUM):
    init_pos = vec(-BRIDGE_LEN/2 - WALL_WIDTH*2*i - 5, PPL_DIM.y, 0)
    
    ppl = Person(start_pos=init_pos, mass = PPL_MASS, vel = PPL_SPEED)
    

#########################
# INIT PLANKS
#########################

plank_list = []

class Plank:
    def __init__(self, start_pos, mass, length=10.0, height = 2.0, width=50.0):
        self.pos = start_pos
        self.mass = mass
        self.velocity = vec(0, 0, 0)
        self.net_force = vec(0, 0, 0)

        self.model = box(
            texture=textures.wood,
            pos=self.pos,
            size=vec(length, height, width),
            color=vec(0.5, 0.25, 0)
        )
        
for i in range(PLA_NUM):
    init_pos = vec(5-BRIDGE_LEN/2 + (i*PLA_WIDTH), 0, 0)
    pla = Plank(start_pos=init_pos, mass=5.0)
    
    if i==0 or i==PLA_NUM-1:
        pla.anchored = True
    else:
        pla.anchored = False
        
    plank_list.append(pla)
        
#########################
# INIT SPRINGS
#########################        

spring_list = []


class Spring:
    def __init__(self, k, plankL, plankR):
        self.k = k
        self.plank_A = plankL
        self.plank_B = plankR
        
        self.rest_length = mag(plankL.model.pos - plankR.model.pos)
        
        self.model = helix(
            pos=plankL.model.pos,
            axis = (plankR.model.pos - plankL.model.pos), 
            radius = 0.5, coils = 8, thickness=0.3, color=color.gray(0.6)
        )

spring_list = []

num_planks = 12
gap = 8.0 
start_x = -44

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
# EXTRANEOUS VISUALS
#########################

# outline
if (extra_visuals):
    
    outline_w,outline_h,outline_d = BRIDGE_LEN/2, 50, 50
    
    for s1 in (-1, 1):
        for s2 in (-1, 1):
            curve(pos=[vec(-outline_w, s1*outline_h, s2*outline_d), vec(outline_w, s1*outline_h, s2*outline_d)], color=color.black, radius=0.2)  # along x
            curve(pos=[vec(s1*outline_w, -outline_h, s2*outline_d), vec(s1*outline_w, outline_h, s2*outline_d)], color=color.black, radius=0.2)  # along y
            curve(pos=[vec(s1*outline_w, s2*outline_h, -outline_d), vec(s1*outline_w, s2*outline_h, outline_d)], color=color.black, radius=0.2)  # along z    

    # axes
    arrow(pos=vec(0, 0, 0), axis=vec(30, 0, 0), color=color.orange, shaftwidth=1.0)
    arrow(pos=vec(0, 0, 0), axis=vec(0, 30, 0), color=color.cyan, shaftwidth=1.0)
    arrow(pos=vec(0, 0, 0), axis=vec(0, 0, 30), color=color.white, shaftwidth=1.0)
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
#########################|
t = 0
dt = 0.01
g = vec(0, -9.8, 0)
b = 1.0 

while True:
    rate(30)
    t+=dt
    for s in spring_list:
        spring_vec = s.plank_B.model.pos - s.plank_A.model.pos
        current_length = mag(spring_vec)
        
        if current_length > 0: 
            spring_dir = norm(spring_vec) 
        else:
            spring_dir = vec(0,0,0)

        stretch = current_length - s.rest_length
        tension_mag = s.k * stretch

        force_on_A = tension_mag * spring_dir
        force_on_B = -tension_mag * spring_dir

        s.plank_A.net_force += force_on_A
        s.plank_B.net_force += force_on_B
        
        s.model.pos = s.plank_A.model.pos
        s.model.axis = spring_vec

    for p in plank_list:
        if not p.anchored:
            p.net_force += p.mass * g 
            p.net_force -= b * p.velocity
            acceleration = p.net_force / p.mass
            p.velocity += acceleration * dt
            p.model.pos += p.velocity * dt      
        p.net_force = vec(0,0,0)
        
    print(plank_list[5].model.pos)
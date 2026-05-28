import warnings
warnings.filterwarnings("ignore", message="pkg_resources is deprecated")
from vpython import *

# Web VPython 3.2

#########################
# NO-LIB HELPER FUNCTIONS
#########################
v=3
def rand():
    global v
    v = (1103515245 * v + 12345) % (2**31)
    return v/(2**31)

pi=3.141592
def sin(x):
    x = ((x + pi) % (2*pi)) - pi
    return x - (x**3)/6 + (x**5)/120
def cos(x):
    return sin(x + pi/2)

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

p1 = Plank(start_pos=vec(0,0,0), mass=3.0)
plank_list.append(p1)

class Spring:
    def __init__(self, k):
        self.k = k

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
box(pos=vec(-50, -25, 0), length=5, height=50, width=100)
box(pos=vec(50, -25, 0), length=5, height=50, width=100)

#########################
# LIGHT SETUP
#########################

num_LL = 8
r_LL = 33
LLs = []

for i in range(num_LL):
    angle = 2*pi*i/num_LL
    LL = local_light(pos=vec(r_LL*cos(angle), 0, r_LL*sin(angle)), color=vec(rand(), rand(), rand()))
    LLs.append(LL)
    
#scene = canvas(width=800, height=600, background=color.black)
#floor = box(pos=vec(0, -5, 0), size=vec(15, 0.1, 10), color=color.white, opacity=1)

#########################
# MAIN LOOP
#########################
t=0
while True:
    rate(30)
    t+=0.01
    for i in range( 0, len(LLs) ):
        LL = LLs[i]
        angle = t + (2 * pi * i / len(LLs))
        
        LL.pos = vec(r_LL*cos(angle),r_LL*sin(2*t+i/pi), r_LL*sin(angle))
        LL.color = vec(rand(), rand(), rand())


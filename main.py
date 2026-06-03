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

PPL_NUM = 3
PPL_MASS = 5 # kg
PPL_SPEED = 10 # m/s

PLA_NUM = 10

SPR_K = 50 # N/m
SPR_NUM = 1 # in parallel between each
SPR_TYPE = 0 # defaults to torsion type
SPR_MAT = 0 # defaults to aluminum
SPR_B = 10 # dampening constant

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

WALL_L = box(pos=vec(-BRIDGE_LEN/2 -WALL_WIDTH*PPL_NUM, -25, 0), size=vec(WALL_WIDTH*2*PPL_NUM, 50, 100)) # people start from here
WALL_R = box(pos=vec(BRIDGE_LEN/2 + WALL_WIDTH*PPL_NUM, -25, 0), size=vec(WALL_WIDTH*2*PPL_NUM, 50, 100)) # +10 is to fill edge due to floor's size.y
FLOOR = box(pos=vec(0, -50, 0), size=vec(BRIDGE_LEN + 4*WALL_WIDTH*PPL_NUM, 10, 100))

#########################
# INIT PEOPLE
#########################

person_list = []

PPL_DIM = vec(5,10,5) # dimension of person
class Person:
    def __init__(self, start_pos, mass):
        self.pos = start_pos
        self.mass = mass
        self.vel = vec(0,0,0) # vec(PPL_SPEED,0,0)
        
        self.model = ellipsoid(
            texture = textures.wood,
            pos = self.pos,
            size = PPL_DIM,
            color = vec(0,0,0)
        )
        
def init_people():
    global person_list
    
    first_init = len(person_list)==0
    
    for i in range(PPL_NUM):
        init_pos = vec(-BRIDGE_LEN/2 - WALL_WIDTH*2*i - 5, PPL_DIM.y/2, 0)
        if first_init:
            ppl = Person(start_pos=init_pos, mass = PPL_MASS)
            person_list.append(ppl)
        else:
            person_list[i].pos = init_pos
            person_list[i].model.pos = init_pos
            person_list[i].model.visible = True

#########################
# INIT PLANKS
#########################

plank_list = []

class Plank:
    def __init__(self, start_pos, mass, length=PLA_WIDTH, height = 2.0, width=50.0):
        self.pos = start_pos
        self.mass = mass
        self.velocity = vec(0, 0, 0)
        self.net_force = vec(0, 0, 0)
        
        self.angle = 0

        self.model = box(
            texture=textures.wood,
            pos=self.pos,
            size=vec(length, height, width),
            color=vec(0.5, 0.25, 0)
        )

def init_planks():
    global plank_list
    
    first_init = len(plank_list)==0
    
    for i in range(PLA_NUM):
        init_pos = vec(-BRIDGE_LEN/2 + (i+0.5)*PLA_WIDTH, -1, 0)
        if first_init:
            pla = Plank(start_pos=init_pos, mass=5.0)
            
            if i==0 or i==PLA_NUM-1:
                pla.anchored = True
            else:
                pla.anchored = False
                
            plank_list.append(pla)
        else:
            plank_list[i].model.pos = init_pos
            plank_list[i].pos = init_pos
            plank_list[i].velocity = vec(0,0,0)
            plank_list[i].acceleration = vec(0,0,0)

            plank_list[i].model.visible = True
        
#########################
# INIT SPRINGS
#########################        

spring_list = []

class Spring:
    def __init__(self, k, plankL, plankR):
        self.k = k
        self.plankL = plankL
        self.plankR = plankR
        
        self.rest_length = mag(plankL.model.pos - plankR.model.pos)
        
        self.model = helix(
            pos=plankL.model.pos,
            axis = (plankR.model.pos - plankL.model.pos), 
            radius = 0.5, coils = 8, thickness=0.3, color=color.gray(0.6)
        )

def init_springs():
    global spring_list
    
    first_init = len(spring_list)==0
    
    for i in range(PLA_NUM-1):
        if first_init:
            s = Spring(k=200, plankL = plank_list[i], plankR = plank_list[i+1])
            spring_list.append(s)
        else:
            spring_list[i].angle = 0
            spring_list[i].model.pos = spring_list[i].plankL.model.pos
            spring_list[i].model.axis = spring_list[i].plankR.model.pos - spring_list[i].plankL.model.pos
            spring_list[i].rest_length = mag(spring_list[i].plankR.model.pos - spring_list[i].plankL.model.pos)
            spring_list[i].model.visible = True
    
#########################
# EXTRANEOUS VISUALS
#########################

# outline
if (extra_visuals):
    
    outline_w,outline_h,outline_d = BRIDGE_LEN/2, 45, 50
    
    for s1 in (-1, 1):
        for s2 in (-1, 1):
            curve(pos=[vec(-outline_w, s1*outline_h, s2*outline_d), vec(outline_w, s1*outline_h, s2*outline_d)], color=color.black, radius=0.2)  # along x
            curve(pos=[vec(s1*outline_w, -outline_h, s2*outline_d), vec(s1*outline_w, outline_h, s2*outline_d)], color=color.black, radius=0.2)  # along y
            curve(pos=[vec(s1*outline_w, s2*outline_h, -outline_d), vec(s1*outline_w, s2*outline_h, outline_d)], color=color.black, radius=0.2)  # along z    

    # axes
    arrow(pos=vec(0, 0, 0), axis=vec(30, 0, 0), color=color.orange, shaftwidth=1.0)
    arrow(pos=vec(0, 0, 0), axis=vec(0, 30, 0), color=color.cyan, shaftwidth=1.0)
    arrow(pos=vec(0, 0, 0), axis=vec(0, 0, 30), color=color.white, shaftwidth=1.0)

#########################
# MAIN BUTTONS
#########################
go = False

def advance():
    global person_list
    global BUTTON_PPL
    
    for person in person_list:
        person.vel = vec(PPL_SPEED,0,0)
    
    BUTTON_PPL.delete()
    BUTTON_PPL = button(bind=cease, text = 'CEASE', background=color.red)
        
def cease():
    global person_list
    global BUTTON_PPL
    
    for person in person_list:
        person.vel = vec(0,0,0)
        
    BUTTON_PPL.delete()
    BUTTON_PPL = button(bind=advance, text = 'ADVANCE', background=color.green)

def start():
    global BUTTON_MAIN
    global BUTTON_PPL
    global go
    init_people()
    init_planks()
    init_springs()
    go = True
    BUTTON_MAIN.delete()
    BUTTON_MAIN = button(bind=stop, text='RESET', background=color.red)
    BUTTON_PPL = button(bind=advance, text = 'ADVANCE', background=color.green)
    
    # ADD: start() updates certain buttons to be available

def stop():
    global BUTTON_MAIN
    global BUTTON_PPL
    global go
    global person_list
    global plank_list
    global spring_list
    
    for ppl in person_list:
        ppl.model.visible = False
    
    for pla in plank_list:
        pla.model.visible = False
        
    for spr in spring_list:
        spr.model.visible = False

    go = False
    BUTTON_MAIN.delete()
    BUTTON_MAIN = button(bind=start, text='START', background=color.green)
    BUTTON_PPL.delete()
    
    # ADD: stop() updates certain buttons to be available

BUTTON_MAIN = button(bind=start, text='START', background=color.green)

#########################
# MAIN
#########################

t=0
dt=0.01
g = vec(0,-9.8,0)

while True:
    rate(30)
    t+=dt
    
    if not go: continue

    #########################
    # MAIN PHYSICS CALCULATIONS
    #########################
    
    for p in plank_list:
        p.net_force = vec(0, 0, 0)
    
    for s in spring_list:
        spring_vec = s.plankR.model.pos - s.plankL.model.pos
        current_length = mag(spring_vec)
        
        if current_length > 0: 
            spring_dir = norm(spring_vec) 
        else:
            spring_dir = vec(0,0,0)

        stretch = current_length - s.rest_length
        tension_mag = s.k * stretch

        s.plankL.net_force += tension_mag * spring_dir
        s.plankR.net_force += -tension_mag * spring_dir
        
        s.model.pos = s.plankL.model.pos
        s.model.axis = spring_vec
        
    for person in person_list:
                
        # check stopped here
            
        person.model.pos += person.vel * dt
        
        on_bridge = abs(p.model.pos.x) < BRIDGE_LEN/2
        if on_bridge:            
            for p in plank_list:
                if (p.model.pos.x - p.model.size.x/2) <= person.model.pos.x <= (p.model.pos.x + p.model.size.x/2):
                    p.net_force += vec(0, -person.mass * 9.8, 0)
                    
                    dx = person.model.pos.x - p.model.pos.x
                    surface_y = p.model.pos.y + dx * tan(p.angle) + (p.model.size.y/2)/cos(p.angle)
                    person.model.pos.y = surface_y + person.model.size.y/2
                    break
                
        if not on_bridge: 
            person.model.pos.y = PPL_DIM.y/2

    for p in plank_list:
        if not p.anchored:
            p.net_force += p.mass * g 
            p.net_force -= SPR_B * p.velocity
            acceleration = p.net_force / p.mass
            p.velocity += acceleration * dt
            p.model.pos += p.velocity * dt

    for i in range(len(plank_list)):
        p = plank_list[i]
        pL = plank_list[i-1] if i>0 else None
        pR = plank_list[i+1] if i<len(plank_list)-1 else None
        
        distinguish = 1 if pR is None else (-1 if pL is None else 0)

        if pR is None:
            slope_vec = p.model.pos - plank_list[i-2].model.pos
            pivot = vec(BRIDGE_LEN/2, 0, 0)   # right wall anchor point
        elif pL is None:
            slope_vec = plank_list[i+2].model.pos - p.model.pos
            pivot = vec(-BRIDGE_LEN/2, 0, 0)  # left wall anchor point
        else:
            slope_vec = pR.model.pos - pL.model.pos
            pivot = p.model.pos
    
    
        if mag(slope_vec) == 0: continue
        theta = atan2(slope_vec.y, slope_vec.x)
        p.model.rotate(angle=theta - p.angle, axis=vec(0, 0, 1), origin=pivot)
        p.angle = theta
    
    print(plank_list[PLA_NUM/2].model.pos)

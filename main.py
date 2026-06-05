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

WALL_WIDTH = 10

BREAK_THRESHOLDS = [
    [18.0, 22.0, 12.0],   # steel
    [12.0, 15.0,  8.0],   # aluminum
    [10.0, 13.0,  7.0],   # bronze
]

#########################
# INPUTS
#########################

PPL_NUM = 3
PPL_MASS = 5 # kg
PPL_SPEED = 5 # m/s

PLA_NUM = 10

SPR_K = 250 # N/m
SPR_NUM = 1 # in parallel between each
SPR_TYPE = 0 # defaults to torsion type
SPR_MAT = 0 # defaults to aluminum
SPR_B = 2 # dampening constant

extra_visuals = False

#########################
# INPUT WIDGETS
#########################

def widget():
    scene.select()
    
    scene.append_to_caption("<b>Parameters</b>\n\n")
    
    scene.append_to_caption("<b>--- People ---</b>\n")
    
    scene.append_to_caption("# People: ")
    def set_ppl_num(s):
        global PPL_NUM
        nonlocal ppl_num_label
        PPL_NUM = int(s.number)
        ppl_num_label.text = f'{int(s.number)}'
    slider(min=1, max=10, value=PPL_NUM, step=1, length=180, bind=set_ppl_num)
    ppl_num_label = wtext(text=f'{PPL_NUM}')
    
    scene.append_to_caption("\nMass (kg): ")
    def set_ppl_mass(s):
        global PPL_MASS
        nonlocal ppl_mass_label
        PPL_MASS = s.number
        ppl_mass_label.text = f'{s.number:.1f}'
    slider(min=1, max=200, value=PPL_MASS, step=1, length=180, bind=set_ppl_mass)
    ppl_mass_label = wtext(text=f'{PPL_MASS:.1f}')
    
    scene.append_to_caption("\nSpeed (m/s): ")
    def set_ppl_speed(s):
        global PPL_SPEED
        PPL_SPEED = s.number
        ppl_speed_label.text = f'{s.number:.1f}'
    slider(min=1, max=20, value=PPL_SPEED, step=0.5, length=180, bind=set_ppl_speed)
    ppl_speed_label = wtext(text=f'{PPL_SPEED:.1f}')
    
    scene.append_to_caption("\n\n<b>--- Planks ---</b>\n")
    
    scene.append_to_caption("# Planks: ")
    def set_pla_num(s):
        global PLA_NUM
        PLA_NUM = int(s.number)
        pla_num_label.text = f'{int(s.number)}'
    slider(min=4, max=20, value=PLA_NUM, step=1, length=180, bind=set_pla_num)
    pla_num_label = wtext(text=f'{PLA_NUM}')
    
    scene.append_to_caption("\n\n<b>--- Springs ---</b>\n")
    
    scene.append_to_caption("k (N/m): ")
    def set_spr_k(s):
        global SPR_K
        SPR_K = s.number
        spr_k_label.text = f'{s.number:.0f}'
    slider(min=100, max=500, value=SPR_K, step=10, length=180, bind=set_spr_k)
    spr_k_label = wtext(text=f'{SPR_K:.0f}')
    
    scene.append_to_caption("\nParallel #: ")
    def set_spr_num(s):
        global SPR_NUM
        SPR_NUM = int(s.number)
        spr_num_label.text = f'{int(s.number)}'
    slider(min=1, max=5, value=SPR_NUM, step=1, length=180, bind=set_spr_num)
    spr_num_label = wtext(text=f'{SPR_NUM}')
    
    scene.append_to_caption("\nDamping b: ")
    def set_spr_b(s):
        global SPR_B
        SPR_B = s.number
        spr_b_label.text = f'{s.number:.1f}'
    slider(min=0, max=20, value=SPR_B, step=1, length=180, bind=set_spr_b)
    spr_b_label = wtext(text=f'{SPR_B:.1f}')
    
    scene.append_to_caption("\n\nType: ")
    def set_spr_type(m):
        global SPR_TYPE
        SPR_TYPE = m.index
    menu(choices=["Torsion", "Tension", "Compression"], index=SPR_TYPE, bind=set_spr_type)
    
    scene.append_to_caption("  Mat: ")
    def set_spr_mat(m):
        global SPR_MAT
        SPR_MAT = m.index
    menu(choices=["Steel", "Aluminum", "Bronze"], index=SPR_MAT, bind=set_spr_mat)
    
    scene.append_to_caption("\n\n")


#########################
# SCENE SETUP
#########################

#scene.userzoom = False
#scene.resizable = False
scene.length = 10
scene.width = 1000
scene.background = color.white
scene.title = "<b>PHYSICS FINAL PROJECT: Spring Bridge</b>"

scene.select()
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

PPL_DIM = vec(10,20,10) # dimension of person
class Person:
    def __init__(self, start_pos, mass):
        self.mass = mass
        self.vel = vec(0,0,0) # vec(PPL_SPEED,0,0)
        
        self.model = box(
            texture = textures.wood,
            pos = start_pos,
            size = PPL_DIM,
            color = vec(0,0,0)
        )
        
def init_people():
    global person_list
    
    # temp
    for ppl in person_list:
        ppl.model.visible = False
    person_list = []

    
    first_init = len(person_list)==0
    
    for i in range(PPL_NUM):
        init_pos = vec(-BRIDGE_LEN/2 - WALL_WIDTH*2*i - 5, PPL_DIM.y/2, 0)
        if first_init:
            ppl = Person(start_pos=init_pos, mass = PPL_MASS)
            person_list.append(ppl)
        else:
            person_list[i].model.pos = init_pos
            person_list[i].model.visible = True

#########################
# INIT PLANKS
#########################

plank_list = []

class Plank:
    def __init__(self, start_pos, mass, length=PLA_WIDTH, height = 2.0, width=50.0):
        self.mass = mass
        self.velocity = vec(0, 0, 0)
        self.net_force = vec(0, 0, 0)
        
        self.angle = 0

        self.model = box(
            texture=textures.wood,
            pos=start_pos,
            size=vec(length, height, width),
            color=vec(0.5, 0.25, 0)
        )

def init_planks():
    global plank_list
    
    # temp
    for pla in plank_list:
        pla.model.visible = False
    plank_list = []

    
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
        self.broken = False
        self.break_threshold = BREAK_THRESHOLDS[SPR_MAT][SPR_TYPE]
        
        self.rest_length = mag(plankL.model.pos - plankR.model.pos)
        
        self.model = helix(
            pos=plankL.model.pos,
            axis = (plankR.model.pos - plankL.model.pos), 
            radius = 0.5, coils = 8, thickness=0.3, color=color.gray(0.6)
        )

def init_springs():
    global spring_list

    for spr in spring_list:
        spr.model.visible = False
    spring_list = []

    first_init = len(spring_list)==0
    
    for i in range(PLA_NUM-1):
        if first_init:
            s = Spring(k=SPR_K*SPR_NUM, plankL = plank_list[i], plankR = plank_list[i+1])
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
# GRAPH SETUP
#########################
disp_graph = graph(title="<b>Center Plank Displacement</b>", xtitle="Time (s)", ytitle="Y-Position (m)", width=1000, height=250)
disp_curve = gcurve(color=color.red, width=2)

energy_graph = graph(title="<b>System Energy</b>", xtitle="Time (s)", ytitle="Energy (Joules)", width=1000, height=250)
ke_curve = gcurve(graph=energy_graph, color=color.blue, label="Kinetic E.")
pe_curve = gcurve(graph=energy_graph, color=color.green, label="Potential E.")
te_curve = gcurve(graph=energy_graph, color=color.black, label="Total E.")


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
    BUTTON_PPL = button(bind=cease, text = 'CEASE\n', background=color.red)
        
def cease():
    global person_list
    global BUTTON_PPL
    
    for person in person_list:
        person.vel = vec(0,0,0)
        
    BUTTON_PPL.delete()
    BUTTON_PPL = button(bind=advance, text = 'ADVANCE\n', background=color.green)

def start():
    global BUTTON_MAIN, BUTTON_PPL, go , t
    global BRIDGE_LEN, WALL_L, WALL_R, FLOOR

    BRIDGE_LEN = PLA_WIDTH * PLA_NUM
    WALL_L.pos = vec(-BRIDGE_LEN/2 - WALL_WIDTH*PPL_NUM, -25, 0)
    WALL_L.size = vec(WALL_WIDTH*2*PPL_NUM, 50, 100)
    WALL_R.pos = vec(BRIDGE_LEN/2 + WALL_WIDTH*PPL_NUM, -25, 0)
    WALL_R.size = vec(WALL_WIDTH*2*PPL_NUM, 50, 100)
    FLOOR.size = vec(BRIDGE_LEN + 4*WALL_WIDTH*PPL_NUM, 10, 100)

    init_people()
    init_planks()
    init_springs()
    go = True
    t = 0
    disp_curve.data = []
    ke_curve.data = []
    pe_curve.data = []
    te_curve.data = []
    BUTTON_MAIN.delete()
    BUTTON_MAIN = button(bind=stop, text='RESET\n', background=color.red)
    BUTTON_PPL = button(bind=advance, text = 'ADVANCE\n', background=color.green)
    
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
    BUTTON_MAIN = button(bind=start, text='START\n', background=color.green)
    BUTTON_PPL.delete()
    
    # ADD: stop() updates certain buttons to be available
widget()

BUTTON_MAIN = button(bind=start, text='START\n', background=color.green)

#########################
# MAIN
#########################

t=0
dt=0.01
g = vec(0,-9.8,0)

while True:
    rate(100)
    t+=dt
    
    if not go: continue

    #########################
    # MAIN PHYSICS CALCULATIONS
    #########################
    
    for p in plank_list:
        p.net_force = vec(0, 0, 0)
    
    for s in spring_list:
        if s.broken:
            s.model.visible = False
            continue

        
        spring_vec = s.plankR.model.pos - s.plankL.model.pos
        current_length = mag(spring_vec)
        
        if current_length > 0: 
            spring_dir = norm(spring_vec) 
        else:
            spring_dir = vec(0,0,0)

        stretch = current_length - s.rest_length
        
        if stretch > s.break_threshold:
            s.broken = True
            s.model.color = color.red
            s.model.visible = False
            continue
        
        
        
        tension_mag = s.k* SPR_NUM   * stretch

        s.plankL.net_force += tension_mag * spring_dir
        s.plankR.net_force += -tension_mag * spring_dir
        
        s.model.pos = s.plankL.model.pos
        s.model.axis = spring_vec
        
        stress_ratio = min(stretch / s.break_threshold, 1.0)
        if stress_ratio < 0.5:
            s.model.color = vec(stress_ratio * 2, 1, 0) # GtY
        else:
            s.model.color = vec(1, 1 - (stress_ratio - 0.5) * 2, 0) # YtR

        
    for person in person_list:
                
        # check stopped here
            
        person.model.pos += person.vel * dt
        
        on_bridge = abs(person.model.pos.x) < BRIDGE_LEN/2
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

    # ENERGY CALCULATIONS & GRAPHING

    sys_ke = 0
    sys_pe_grav = 0
    sys_pe_spring = 0
    
    for p in plank_list:
        if not p.anchored:
            sys_ke += 0.5 * p.mass * (mag(p.velocity)**2)
            sys_pe_grav += p.mass * 9.8 * p.model.pos.y
            
    for s in spring_list:
        stretch = mag(s.plankR.model.pos - s.plankL.model.pos) - s.rest_length
        sys_pe_spring += 0.5 * s.k * (stretch**2)
        
    sys_pe_total = sys_pe_grav + sys_pe_spring
    sys_energy_total = sys_ke + sys_pe_total
    
    ke_curve.plot(t, sys_ke)
    pe_curve.plot(t, sys_pe_total)
    te_curve.plot(t, sys_energy_total)

    # Displacement graphing
    center_index = len(plank_list) // 2
    center_y = plank_list[center_index].model.pos.y
    disp_curve.plot(t, center_y)

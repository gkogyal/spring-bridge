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
STL_MAT = 0
ALM_MAT = 1
BRZ_MAT = 2

PLA_WIDTH = 10
PLA_MASS = 5.0

WALL_WIDTH = 10

BREAK_THRESHOLDS = [
    [18.0, 22.0, 12.0],
    [12.0, 15.0,  8.0],
    [10.0, 13.0,  7.0],
]

#########################
# INPUTS
#########################

PPL_NUM = 7
PPL_MASS = 100
PPL_SPEED = 12

PLA_NUM = 10

SPR_K = 250
SPR_NUM = 1
SPR_TYPE = 0
SPR_MAT = 0
SPR_B = 2

extra_visuals = False

#########################
# GLOBAL STATE
#########################

ppl_moving = False
BUTTON_PPL = None

#########################
# INPUT WIDGETS
#########################

widget_list = []

def enable_widgets():
    for w in widget_list:
        w.disabled = False

def disable_widgets():
    for w in widget_list:
        w.disabled = True

def set_ppl_num(s):
    global PPL_NUM, ppl_num_label
    PPL_NUM = int(s.value)
    ppl_num_label.text = f'{PPL_NUM}'

def set_ppl_mass(s):
    global PPL_MASS, ppl_mass_label
    PPL_MASS = s.value
    ppl_mass_label.text = f'{PPL_MASS:.1f}'

def set_ppl_speed(s):
    global PPL_SPEED, ppl_speed_label
    PPL_SPEED = s.value
    ppl_speed_label.text = f'{PPL_SPEED:.1f}'

def set_pla_num(s):
    global PLA_NUM, pla_num_label
    PLA_NUM = int(s.value)
    pla_num_label.text = f'{PLA_NUM}'

def set_spr_k(s):
    global SPR_K, spr_k_label
    SPR_K = s.value
    spr_k_label.text = f'{SPR_K:.0f}'

def set_spr_num(s):
    global SPR_NUM, spr_num_label
    SPR_NUM = int(s.value)
    spr_num_label.text = f'{SPR_NUM}'

def set_spr_b(s):
    global SPR_B, spr_b_label
    SPR_B = s.value
    spr_b_label.text = f'{SPR_B:.1f}'

def set_spr_type(m):
    global SPR_TYPE
    SPR_TYPE = m.index

def set_spr_mat(m):
    global SPR_MAT
    SPR_MAT = m.index

def create_widgets():
    global ppl_num_label, ppl_mass_label, ppl_speed_label
    global pla_num_label, spr_k_label, spr_num_label, spr_b_label
    scene.select()

    scene.append_to_caption("<b>Parameters</b>\n\n")
    scene.append_to_caption("<b>--- People ---</b>\n")

    scene.append_to_caption("# People: ")
    ppl_num_label = wtext(text=f'{PPL_NUM}')
    widget_list.append(slider(min=1, max=10, value=PPL_NUM, step=1, length=180, bind=set_ppl_num))

    scene.append_to_caption("\nMass (kg): ")
    ppl_mass_label = wtext(text=f'{PPL_MASS:.1f}')
    widget_list.append(slider(min=1, max=200, value=PPL_MASS, step=1, length=180, bind=set_ppl_mass))

    scene.append_to_caption("\nSpeed (m/s): ")
    ppl_speed_label = wtext(text=f'{PPL_SPEED:.1f}')
    widget_list.append(slider(min=1, max=20, value=PPL_SPEED, step=0.5, length=180, bind=set_ppl_speed))

    scene.append_to_caption("\n\n<b>--- Planks ---</b>\n")
    scene.append_to_caption("# Planks: ")
    pla_num_label = wtext(text=f'{PLA_NUM}')
    widget_list.append(slider(min=4, max=20, value=PLA_NUM, step=1, length=180, bind=set_pla_num))

    scene.append_to_caption("\n\n<b>--- Springs ---</b>\n")
    scene.append_to_caption("k (N/m): ")
    spr_k_label = wtext(text=f'{SPR_K:.0f}')
    widget_list.append(slider(min=100, max=500, value=SPR_K, step=10, length=180, bind=set_spr_k))

    scene.append_to_caption("\nParallel #: ")
    spr_num_label = wtext(text=f'{SPR_NUM}')
    widget_list.append(slider(min=1, max=5, value=SPR_NUM, step=1, length=180, bind=set_spr_num))

    scene.append_to_caption("\nDamping b: ")
    spr_b_label = wtext(text=f'{SPR_B:.1f}')
    widget_list.append(slider(min=0, max=20, value=SPR_B, step=1, length=180, bind=set_spr_b))

    scene.append_to_caption("\n\nType: ")
    widget_list.append(menu(choices=["Torsion", "Tension", "Compression"], index=SPR_TYPE, bind=set_spr_type))

    scene.append_to_caption("  Mat: ")
    widget_list.append(menu(choices=["Steel", "Aluminum", "Bronze"], index=SPR_MAT, bind=set_spr_mat))

    scene.append_to_caption("\n\n")

#########################
# SCENE SETUP
#########################

scene.userzoom = False
scene.resizable = False
scene.length = 10
scene.width = 700
scene.height = 400
scene.background = color.white
scene.title = "<b>PHYSICS FINAL PROJECT: Spring Bridge</b>"
scene.select()

#########################
# HEATMAP CANVAS
#########################

MAX_PLANKS = 20
HMAP_W = 260
HMAP_H = 400
HMAP_MARGIN = 4

hmap_scene = canvas(
    title="<b>Force Heatmap</b>",
    width=HMAP_W, height=HMAP_H,
    background=color.white,
    userzoom=False, userspin=False, resizable=False
)

# World coords: cells span Y from +half to -half, X fills width
HMAP_WORLD_H = 20.0 
HMAP_WORLD_W = 10.0
hmap_scene.range = HMAP_WORLD_H * 0.65
hmap_scene.camera.pos  = vec(0, 0, 50)
hmap_scene.camera.axis = vec(0, 0, -1)

CELL_H_WORLD = HMAP_WORLD_H / MAX_PLANKS
CELL_GAP     = CELL_H_WORLD * 0.06

hmap_boxes  = []
hmap_labels = []

for j in range(MAX_PLANKS):
    cy = HMAP_WORLD_H/2 - (j + 0.5) * CELL_H_WORLD
    b = box(
        canvas=hmap_scene,
        pos=vec(0, cy, 0),
        size=vec(HMAP_WORLD_W, CELL_H_WORLD - CELL_GAP, 0.1),
        color=color.gray(0.85),
        visible=False
    )
    hmap_boxes.append(b)
    lbl = label(
        canvas=hmap_scene,
        pos=vec(0, cy, 0.2),
        text='',
        height=8,
        color=color.black,
        box=False,
        opacity=0,
        visible=False
    )
    hmap_labels.append(lbl)

# gradient legend
LEGEND_STEPS = 30
LEG_Y = -(HMAP_WORLD_H/2 + 1.6)
LEG_W = HMAP_WORLD_W
LEG_H = 0.8
for j in range(LEGEND_STEPS):
    t_val = j / (LEGEND_STEPS - 1)
    norm_val = t_val * 2 - 1
    if norm_val <= 0:
        lc = vec(1 + norm_val, 1 + norm_val, 1.0)
    else:
        lc = vec(1.0, 1 - norm_val, 1 - norm_val)
    lx = -LEG_W/2 + (t_val + 0.5/LEGEND_STEPS) * LEG_W
    box(canvas=hmap_scene,
        pos=vec(lx, LEG_Y, 0),
        size=vec(LEG_W/LEGEND_STEPS, LEG_H, 0.1),
        color=lc)

label(canvas=hmap_scene, pos=vec(-LEG_W/2, LEG_Y - 1.1, 0), text='up', height=8, color=color.blue, box=False, opacity=0)
label(canvas=hmap_scene, pos=vec(0, LEG_Y - 1.1, 0), text='0', height=8, color=color.black, box=False, opacity=0)
label(canvas=hmap_scene, pos=vec(LEG_W/2, LEG_Y - 1.1, 0), text='down', height=8, color=color.red, box=False, opacity=0)

# return focus to main scene
scene.select()

# recolors the heatmap cells
def update_heatmap(forces, max_force):
    n = len(forces)
    for i in range(MAX_PLANKS):
        if i < n:
            fy = forces[i]
            norm_v  = max(-1.0, min(1.0, fy / max_force)) if max_force > 0 else 0.0
            if norm_v >= 0:
                c = vec(1 - norm_v, 1 - norm_v, 1.0)
            else:
                a = -norm_v
                c = vec(1.0, 1 - a, 1 - a)
            hmap_boxes[i].color = c
            hmap_boxes[i].visible = True
            hmap_labels[i].text = f'P{i+1}  {fy:.0f}N'
            hmap_labels[i].color = color.black if abs(norm_v) < 0.55 else color.white
            hmap_labels[i].visible = True
        else:
            hmap_boxes[i].visible = False
            hmap_labels[i].visible = False


#########################
# WORLD
#########################

BRIDGE_LEN = PLA_WIDTH * PLA_NUM

WALL_L = box(pos=vec(-BRIDGE_LEN/2 - WALL_WIDTH*PPL_NUM, -25, 0), size=vec(WALL_WIDTH*2*PPL_NUM, 50, 100))
WALL_R = box(pos=vec( BRIDGE_LEN/2 + WALL_WIDTH*PPL_NUM, -25, 0), size=vec(WALL_WIDTH*2*PPL_NUM, 50, 100))

#########################
# PERSON CLASS
#########################

person_list = []
PPL_DIM = vec(10, 20, 10)

class Person:
    def __init__(self, start_pos):
        self.model = box(
            texture=textures.wood,
            pos=start_pos,
            size=PPL_DIM,
            color=vec(0, 0, 0)
        )

def init_people():
    global person_list
    first_init = (len(person_list) == 0)
    for i in range(PPL_NUM):
        init_pos = vec(-BRIDGE_LEN/2 - WALL_WIDTH*2*i - 5, PPL_DIM.y/2, 0)
        if first_init:
            person_list.append(Person(start_pos=init_pos))
        else:
            person_list[i].model.pos = init_pos
            person_list[i].model.visible = True

#########################
# PLANK CLASS
#########################

plank_list = []
plank_force_magnitudes = []   # stores |net_force.y| per plank for heatmap

class Plank:
    def __init__(self, start_pos, length=PLA_WIDTH, height=2.0, width=50.0):
        self.velocity = vec(0, 0, 0)
        self.net_force = vec(0, 0, 0)
        self.angle = 0
        self.anchored = False
        self.model = box(
            texture=textures.wood,
            pos=start_pos,
            size=vec(length, height, width),
            color=vec(0.5, 0.25, 0)
        )

def init_planks():
    global plank_list, plank_force_magnitudes
    first_init = (len(plank_list) == 0)
    for i in range(PLA_NUM):
        init_pos = vec(-BRIDGE_LEN/2 + (i + 0.5)*PLA_WIDTH, -1, 0)
        if first_init:
            pla = Plank(start_pos=init_pos)
            pla.anchored = (i == 0 or i == PLA_NUM - 1)
            plank_list.append(pla)
        else:
            plank_list[i].model.pos = init_pos
            plank_list[i].velocity = vec(0, 0, 0)
            plank_list[i].net_force = vec(0, 0, 0)
            plank_list[i].angle = 0
            plank_list[i].model.visible = True
    plank_force_magnitudes = [0.0] * PLA_NUM

#########################
# SPRING CLASS
#########################

spring_list = []

class Spring:
    def __init__(self, plankL, plankR):
        self.plankL = plankL
        self.plankR = plankR
        self.broken = False
        self.rest_length = mag(plankL.model.pos - plankR.model.pos)
        self.models = []
        self._build_models()

    def _build_models(self):
        n = SPR_NUM
        if n == 1:
            offsets = [0.0]
        else:
            half = 20.0
            offsets = [-half + 2*half*i/(n-1) for i in range(n)]
        ax = self.plankR.model.pos - self.plankL.model.pos
        for z_off in offsets:
            origin = self.plankL.model.pos + vec(0, 0, z_off)
            h = helix(
                pos=origin,
                axis=ax,
                radius=0.5, coils=8, thickness=0.3,
                color=color.gray(0.6)
            )
            self.models.append(h)

    def update_visuals(self, spring_vec, col, visible=True):
        n = SPR_NUM
        if n == 1:
            offsets = [0.0]
        else:
            half = 20.0
            offsets = [-half + 2*half*i/(n-1) for i in range(n)]
        for i, h in enumerate(self.models):
            z_off = offsets[i] if i < len(offsets) else 0.0
            h.pos = self.plankL.model.pos + vec(0, 0, z_off)
            h.axis = spring_vec
            h.color = col
            h.visible = visible

    def hide_all(self):
        for h in self.models:
            h.visible = False


def init_springs():
    global spring_list
    first_init = (len(spring_list) == 0)
    for i in range(PLA_NUM - 1):
        if first_init:
            spring_list.append(Spring(plankL=plank_list[i], plankR=plank_list[i+1]))
        else:
            s = spring_list[i]
            s.broken = False
            s.rest_length = mag(s.plankR.model.pos - s.plankL.model.pos)
            
            # rebvild if SPR_NUM changed
            for h in s.models:
                h.visible = False
            s.models = []
            s._build_models()

#########################
# EXTRA VISUALS
#########################

if extra_visuals:
    ow, oh, od = BRIDGE_LEN/2, 45, 50
    for s1 in (-1, 1):
        for s2 in (-1, 1):
            curve(pos=[vec(-ow, s1*oh, s2*od), vec(ow, s1*oh, s2*od)], color=color.black, radius=0.2)
            curve(pos=[vec(s1*ow, -oh, s2*od), vec(s1*ow, oh, s2*od)], color=color.black, radius=0.2)
            curve(pos=[vec(s1*ow, s2*oh, -od), vec(s1*ow, s2*oh, od)], color=color.black, radius=0.2)
    arrow(pos=vec(0,0,0), axis=vec(30, 0, 0), color=color.orange, shaftwidth=1.0)
    arrow(pos=vec(0,0,0), axis=vec(0, 30, 0), color=color.cyan, shaftwidth=1.0)
    arrow(pos=vec(0,0,0), axis=vec(0, 0, 30), color=color.white, shaftwidth=1.0)

#########################
# GRAPHS
#########################

# --- Graph 1: Center Plank Displacement ---
disp_graph = graph(
    title="<b>Center Plank Displacement</b>",
    xtitle="Time (s)", ytitle="Y-Position (m)",
    width=700, height=220
)
disp_curve = gcurve(color=color.red, width=2)

# --- Graph 2: System Energy ---
energy_graph = graph(
    title="<b>System Energy</b>",
    xtitle="Time (s)", ytitle="Energy (J)",
    width=700, height=220
)
ke_curve   = gcurve(graph=energy_graph, color=color.blue,  label="Kinetic E.")
pe_curve   = gcurve(graph=energy_graph, color=color.green, label="Potential E.")
te_curve   = gcurve(graph=energy_graph, color=color.black, label="Total E.")

# --- Graph 3: Max Spring Stress (fraction of break threshold) ---
stress_graph = graph(
    title="<b>Max Spring Stress  (0 = relaxed · 1 = breaking)</b>",
    xtitle="Time (s)", ytitle="Stress Fraction",
    width=700, height=200,
    ymin=0, ymax=1.1
)
stress_curve = gcurve(graph=stress_graph, color=color.orange, width=2, label="Max stress")

# --- Graph 4: Net Vertical Force per Plank (bar-style) ---
force_graph = graph(
    title="<b>Plank Net Vertical Force</b>",
    xtitle="Plank index", ytitle="Net Fy (N)",
    width=700, height=220,
    xmin=-0.5, xmax=19.5,
    ymin=-2000, ymax=500
)


force_dots = gdots(graph=force_graph, color=color.purple, size=8)


#########################
# BUTTON CALLBACKS
#########################

go = False

def advance():
    global ppl_moving, BUTTON_PPL
    disable_widgets()
    ppl_moving = True
    BUTTON_PPL.delete()
    BUTTON_PPL = button(bind=cease, text='CEASE\n', background=color.red, pos=scene.title_anchor)

def cease():
    global ppl_moving, BUTTON_PPL
    ppl_moving = False
    BUTTON_PPL.delete()
    BUTTON_PPL = button(bind=advance, text='ADVANCE\n', background=color.green, pos=scene.title_anchor)

def start():
    global BUTTON_MAIN, BUTTON_PPL, go, t
    global BRIDGE_LEN, WALL_L, WALL_R

    disable_widgets()

    BRIDGE_LEN = PLA_WIDTH * PLA_NUM
    WALL_L.pos = vec(-BRIDGE_LEN/2 - WALL_WIDTH*PPL_NUM, -25, 0)
    WALL_L.size = vec(WALL_WIDTH*2*PPL_NUM, 50, 100)
    WALL_R.pos = vec(BRIDGE_LEN/2 + WALL_WIDTH*PPL_NUM, -25, 0)
    WALL_R.size = vec(WALL_WIDTH*2*PPL_NUM, 50, 100)

    init_people()
    init_planks()
    init_springs()

    go = True
    t = 0
    disp_curve.data = []
    ke_curve.data = []
    pe_curve.data = []
    te_curve.data = []
    stress_curve.data = []
    force_dots.data = []

    BUTTON_MAIN.delete()
    BUTTON_MAIN = button(bind=stop, text='RESET\n', background=color.red, pos=scene.title_anchor)
    BUTTON_PPL = button(bind=advance, text='ADVANCE\n', background=color.green, pos=scene.title_anchor)

def stop():
    global BUTTON_MAIN, BUTTON_PPL, go, ppl_moving
    global person_list, plank_list, spring_list

    enable_widgets()
    ppl_moving = False
    go = False

    if BUTTON_PPL is not None:
        BUTTON_PPL.delete()
        BUTTON_PPL = None

    for ppl in person_list:
        ppl.model.visible = False
    person_list = []

    for pla in plank_list:
        pla.model.visible = False
    plank_list = []

    for spr in spring_list:
        spr.hide_all()
    spring_list = []

    BUTTON_MAIN.delete()
    BUTTON_MAIN = button(bind=start, text='START\n', background=color.green, pos=scene.title_anchor)

BUTTON_MAIN = button(bind=start, text='START\n', background=color.green, pos=scene.title_anchor)
create_widgets()

#########################
# MAIN LOOP
#########################

t = 0
dt = 0.01
g = vec(0, -9.8, 0)


while True:
    rate(100)
    t += dt

    if not go:
        continue

    k_eff = SPR_K * SPR_NUM
    thresh = BREAK_THRESHOLDS[SPR_MAT][SPR_TYPE]

    for p in plank_list:
        p.net_force = vec(0, 0, 0)

    # -------- Spring forces --------
    max_stress = 0.0
    for s in spring_list:
        if s.broken:
            s.hide_all()
            continue

        spring_vec = s.plankR.model.pos - s.plankL.model.pos
        current_len = mag(spring_vec)
        spring_dir = norm(spring_vec) if current_len > 0 else vec(0, 0, 0)
        stretch = current_len - s.rest_length

        if stretch > thresh:
            s.broken = True
            s.hide_all()
            continue

        tension_mag = k_eff * stretch

        s.plankL.net_force += tension_mag * spring_dir
        s.plankR.net_force -= tension_mag * spring_dir

        stress = min(stretch / thresh, 1.0) if thresh > 0 else 0.0
        if stress > max_stress:
            max_stress = stress

        # Spring color: green → yellow → red based on stress
        if stress < 0.5:
            spr_col = vec(stress * 2, 1, 0)
        else:
            spr_col = vec(1, 1 - (stress - 0.5)*2, 0)

        # Update all parallel helix models
        s.update_visuals(spring_vec, spr_col, visible=True)

    # -------- People movement & weight --------
    for person in person_list:
        if person.model.pos.x >= BRIDGE_LEN/2 + 2*WALL_WIDTH*PPL_NUM - 10:
            ppl_moving = False
            break

        if person.model.pos.y <= -50:
            scene.autoscale = False
            sleep(3)
            stop()
            break

        if ppl_moving:
            person.model.pos.x += PPL_SPEED * dt

        on_bridge = abs(person.model.pos.x) < BRIDGE_LEN/2
        if on_bridge:
            for p in plank_list:
                if (p.model.pos.x - p.model.size.x/2) <= person.model.pos.x <= (p.model.pos.x + p.model.size.x/2):
                    p.net_force += vec(0, -PPL_MASS * 9.8, 0)
                    dx = person.model.pos.x - p.model.pos.x
                    surface_y = p.model.pos.y + dx * tan(p.angle) + (p.model.size.y/2) / cos(p.angle)
                    person.model.pos.y = surface_y + person.model.size.y/2
                    break
        else:
            person.model.pos.y = PPL_DIM.y/2

    if not go:
        continue

    # -------- Plank dynamics --------
    for p in plank_list:
        if not p.anchored:
            p.net_force += PLA_MASS * g
            p.net_force -= SPR_B * p.velocity
            p.velocity += (p.net_force / PLA_MASS) * dt
            p.model.pos += p.velocity * dt

    # -------- Record per-plank F.y for the heatmap and force graph --------
    for i, p in enumerate(plank_list):
        plank_force_magnitudes[i] = p.net_force.y   # signed vertical force

    # -------- Plank rotation --------
    for i in range(len(plank_list)):
        p = plank_list[i]
        pL = plank_list[i-1] if i > 0 else None
        pR = plank_list[i+1] if i < len(plank_list)-1 else None

        if pR is None:
            slope_vec = p.model.pos - plank_list[i-2].model.pos
            pivot = vec(BRIDGE_LEN/2, 0, 0)
        elif pL is None:
            slope_vec = plank_list[i+2].model.pos - p.model.pos
            pivot = vec(-BRIDGE_LEN/2, 0, 0)
        else:
            slope_vec = pR.model.pos - pL.model.pos
            pivot = p.model.pos

        if mag(slope_vec) == 0:
            continue

        theta = atan2(slope_vec.y, slope_vec.x)
        p.model.rotate(angle=theta - p.angle, axis=vec(0, 0, 1), origin=pivot)
        p.angle = theta

    # -------- Energy --------
    sys_ke = 0
    sys_pe_grav = 0
    sys_pe_spring = 0

    for p in plank_list:
        if not p.anchored:
            sys_ke += 0.5 * PLA_MASS * mag(p.velocity)**2
            sys_pe_grav += PLA_MASS * 9.8 * p.model.pos.y

    for s in spring_list:
        stretch = mag(s.plankR.model.pos - s.plankL.model.pos) - s.rest_length
        sys_pe_spring += 0.5 * k_eff * stretch**2

    sys_pe_total = sys_pe_grav + sys_pe_spring
    sys_energy_total = sys_ke + sys_pe_total

    # -------- Plot graphs --------
    ke_curve.plot(t, sys_ke)
    pe_curve.plot(t, sys_pe_total)
    te_curve.plot(t, sys_energy_total)

    center_index = len(plank_list) // 2
    disp_curve.plot(t, plank_list[center_index].model.pos.y)

    # Graph 3: max spring stress
    stress_curve.plot(t, max_stress)

    # Graph 4: force per plank as a scatter (index vs Fy)
    # redrasws all dots each frame using a fresh data list
    new_force_data = []
    for i, fy in enumerate(plank_force_magnitudes):
        new_force_data.append((i, fy))
    force_dots.data = new_force_data

    # -------- Heatmap: update native VPython canvas --------
    max_force_val = max(abs(PPL_MASS * 9.8 * PPL_NUM), 1.0)
    update_heatmap(plank_force_magnitudes, max_force_val)

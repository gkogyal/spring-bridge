import warnings
warnings.filterwarnings("ignore", message="pkg_resources is deprecated")

from vpython import canvas, rate, vec, color, box
from plank import Plank  

scene = canvas(width=800, height=600, background=color.black)
floor = box(pos=vec(0, -5, 0), size=vec(15, 0.1, 10), color=color.white, opacity=1)
test_plank = Plank(start_pos=vec(10, 0, 0), mass=10)
test_plank = Plank(start_pos=vec(8, 0, 0), mass=10)

while True:
    rate(60) 
    pass
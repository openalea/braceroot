from math import cos, sin, degrees, radians
import numpy as np
from braceroot import brace_root, mechanic

stem_height = 10.
angle = [110., 140.]
stem_diameter = [1., 2.]
br_diameter = [0.1, 0.7]
break_strength = [8., 75.]
displacement = [0.5, 5]

# whorls
#W1
root_length1 = [8.5, 19.]
length_above_soil1 = [1.2, 2.3]
root_number1 = [8, 20]

root_length2 = [8.5, 17.5]
length_above_soil2 = [1.5, 7.]
root_number2 = [8, 20]

def select(values):
    return np.random.uniform(*values)

def height(angle, length):
    a = 180-angle
    return length * cos(radians(a))


def run(angle=angle, length_above_soil= [length_above_soil1, length_above_soil2],
        root_number=[root_number1, root_number2],
        stem_diameter=stem_diameter,
        root_length=[root_length1, root_length2],
        root_diameter=br_diameter,
        wind_force=42.,
        seed=1):
    """ Select based on distribution the value of each parameters.
    Adapt the parameters to the model.
    """
    np.random.seed(seed)

    a1= select(angle)
    a2= select(angle)
    las1 = select(length_above_soil[0])
    las2 = select(length_above_soil[1])
    las2 = max(las1+1., las2)

    h1 = height(a1, las1)
    h2 = height(a2, las2)

    nb_root1 = int(select(root_number[0]))
    nb_root2 = int(select(root_number[1]))

    stem_radius = select(stem_diameter)/2.

    rl1 = select(root_length[0])
    rl2 = select(root_length[1])
    rl1 = min(rl1, rl2)
    rl2 = max(rl1, rl2)

    visible1 = las1/rl1
    visible2 = las2/rl2

    rd1 = select(root_diameter)
    rd2 = select(root_diameter)
    br = brace_root.brace_roots(nb_whorl=2,
                     whorl_heights=[h1, h2],
                     nb_root=[nb_root1, nb_root2],
                     whorl_stem_radius= [stem_radius]*2,
                     root_angle = [a1, a2],
                     root_length =[rl1, rl2],
                     visible_ratio=[visible1, visible2],
                     root_diameter = [rd1, rd2],
                     root_stiffness=[0.6,0.6],
                     )

    print(br)
    scene = brace_root.view3d(br, stem_height=10., stem=True)

    final = mechanic.mechanics(br, wind_force)

    scene = brace_root.view3d(br, stem_height=stem_height, stem=True, stalk_angle=final)

    return scene



""" Test the brace root model with simple hypotheses.

1. Test geometry
2. Test without wind nor brace root
3. Test without brace root but with wind
4. Test increasing wind forc linearly for small displacement
5. Test with one whorl, two and three.
"""

from math import cos, sin, degrees, radians
import numpy as np
from braceroot import brace_root, mechanic

def no_whorl():
    """ Test the geometry of the brace root model. 
    Here we test only one whorl. 
    """
    nb_whorl = 0
    br = brace_root.brace_roots(nb_whorl=nb_whorl)
    return br

def one_whorl():
    nb_whorl = 1
    whorl_height = 0.02 # 2 cm
    whorl_stem_radius = 0.02 # 2 cm
    root_length = 0.15 # or 15 cm
    root_diameter = 0.03 # 1 cm
    br = brace_root.brace_roots(nb_whorl=nb_whorl,                      
                     whorl_heights=[whorl_height, 0.],
                     nb_root=[10, 0],
                     whorl_stem_radius= None,
                     root_angle = [110., 140.],
                     root_length =[root_length]*2,
                     visible_ratio=[0.2, 0.8],
                     root_diameter = [root_diameter]*2,
                     root_stiffness=[600,600],
                     )
    return br

def two_whorl():
    nb_whorl = 2
    whorl_height = 0.02 # 2 cm
    whorl_stem_radius = 0.02 # 2 cm
    root_length = 0.15 # or 15 cm
    root_diameter = 0.03 # 1 cm
    br = brace_root.brace_roots(nb_whorl=nb_whorl,                      
                     whorl_heights=[whorl_height, 3*whorl_height],
                     nb_root=[10, 10],
                     whorl_stem_radius= None,
                     root_angle = [110., 110.], # not used
                     root_length =[root_length]*2,
                     visible_ratio=[0.2, 0.8],
                     root_diameter = [root_diameter]*2,
                     root_stiffness=[600,600],
                     )
    return br


def test_weight_only():
    """ Test the geometry of the brace root model. 
    Here we test only one whorl. 
    """
    br = no_whorl()
    final_angle = mechanic.mechanics(br, 0., stem_height=1., stem_mass=1., stalk_stiffness=160.)
    assert final_angle == 0.
    print(final_angle)

def test_geometry():
    """ Test the geometry of the brace root model. 
    Here we test only one whorl. 
    """
    stem_height = 1. #m
    br = one_whorl()

    final_angle = mechanic.mechanics(br, 0., stem_height=stem_height, stem_mass=1., stalk_stiffness=160.)
    scene = brace_root.view3d(br, stem_height=stem_height, stem=True, stalk_angle=final_angle)

    # What do we want to test?
    return scene

def test_geometry2():
    """ Test the geometry of the brace root model. 
    Here we test two whorls. 
    """
    stem_height = 1. #m
    br = two_whorl()

    final_angle = mechanic.mechanics(br, 0., stem_height=stem_height, stem_mass=1., stalk_stiffness=160.)
    scene = brace_root.view3d(br, stem_height=stem_height, stem=True, stalk_angle=final_angle)
    return scene


def test_meca0():
    """ First we test without brace root.
    """
    stem_height = 1.
    br = no_whorl()
    angles = []
    for i in range(10):
        angle = mechanic.mechanics(br, wind_force=i, stem_height=stem_height, stem_mass=1., stalk_stiffness=160.)
        angles.append(degrees(angle))

    print("Angles are: "+ ' '.join(map(str,angles)))

def test_meca1(wind_factor=1., nb_whorl=0):
    """ First we test without brace root.
    """
    stem_height = 1.
    if nb_whorl == 0:
        br = no_whorl()
    elif nb_whorl == 1:
        br = one_whorl()
    else: 
        br = two_whorl()

    angles = []
    for i in range(10):
        angle = mechanic.mechanics(br, wind_force=wind_factor*i, stem_height=stem_height, stem_mass=1., stalk_stiffness=160.)
        angles.append(degrees(angle))

    print("Angles are: "+ ' '.join(map(str,angles)))

def test_debug1():
    stem_height = 1.
    br = one_whorl()
    angles = []
    for i in range(10):
        angle, scene = mechanic.mechanics(br, wind_force=i, stem_height=stem_height, stem_mass=1., stalk_stiffness=160., debug=True)
        angles.append(degrees(angle))

        bbs=scene['whorl0']
        for bb in bbs:
            print('Moment ', bb.moment())
    print("Angles are: "+ ' '.join(map(str,angles)))

def test_debug1_strong(wind_factor=1., one=1):
    stem_height = 1.
    if one==1:
        br = one_whorl()
    elif one ==0:
        br = no_whorl()
    else:
        br = two_whorl()
    angles = []
    for i in range(10):
        angle, scene = mechanic.mechanics(br, wind_force=wind_factor*i, stem_height=stem_height, stem_mass=1., stalk_stiffness=160., debug=True)
        angles.append(degrees(angle))
        if one:
            bbs=scene['whorl0']
            for bb in bbs:
                print('Moment ', bb.moment())
    print("Angles are: "+ ' '.join(map(str,angles)))

def test_brace_root_contribution():
    br0 = no_whorl()
    br1 = one_whorl()
    br2 = two_whorl()

    wind_force = 10. #N
    stem_height = 1.
    stem_mass = 1.
    stalk_stiffness = 160.

    def meca(br, debug=False):
        return mechanic.mechanics(
            br, 
            wind_force=wind_force, 
            stem_height=stem_height,
            stem_mass=stem_mass,
            stalk_stiffness=stalk_stiffness,
            debug=debug)
    
    a0 = degrees(meca(br0))
    a1 = degrees(meca(br1))
    a2 = degrees(meca(br2))


    _a2, scene = meca(br2, debug=True)
    
    bbs=scene['whorl0']
    forces = [bb.force() for bb in bbs]
    moments = [bb.moment() for bb in bbs]
    print("Forces whorl0: ", forces)
    print("Moments whorl0: ", moments)
    assert abs(a0) >= abs(a1)
    assert abs(a1) >= abs(a2)

    print ("Angles: ", a0, a1, a2)
    


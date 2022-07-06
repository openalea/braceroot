""" Test the brace root object .
 three.
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


def whorls(whorl=(0,0,0), nb_root=10, stiffness=600. ):
    if whorl==(0,0,0):
        return no_whorl()

    nb_whorl = 3 if whorl[2] else 2 if whorl[1] else 1

    #whorl_height = 0.02 # 2 cm
    #whorl_stem_radius = 0.02 # 2 cm
    root_length = 0.15 # or 15 cm
    root_diameter = 0.03 # 3 cm
    
    nb_root = [10*w for w in whorl]
    whorl_heights = [0.02, 0.05, 0.1] # meter
    root_angle = [135., 135., 135.]
    root_diameters = [root_diameter]*3
    root_stiffness = [stiffness]*3
    br = brace_root.brace_roots(
        nb_whorl=nb_whorl,                      
        whorl_heights=whorl_heights,
        nb_root=nb_root,
        whorl_stem_radius=None,
        root_angle=root_angle,
        root_length=[root_length]*3,
        visible_ratio=[0.2, 0.36, 0.68],
        root_diameter= root_diameters,
        root_stiffness=root_stiffness
        )
    return br

def test_br2_1():
    "Test Brace root 2 without 1 whorl"

    br2_1 = whorls(whorl=(0,1,0))
    assert(len(br2_1['root_stiffness'][1])==10)
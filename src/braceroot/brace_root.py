""" A collection of simple allometric functions for parameterising the
architecture of maize"""

import atexit
import os
import math
from turtle import st
import numpy as np
from itertools import cycle

from openalea.plantgl.all import *

################################

def brace_curve(height, length, visible_ratio, angles, stem_radius, phyllotaxis=0.):
    """ Compute tangency based on the angles.
    Add visible length vs length.

    """
    cp = math.cos(math.radians(phyllotaxis))
    sp = math.sin(math.radians(phyllotaxis))
    r = stem_radius
    aerial_length = max(length * visible_ratio, height)
    pt0 = (r*cp, r*sp, height)
    x = math.sqrt(aerial_length**2 - height**2) + r
    pt1 = (x * cp, x * sp, 0.)
    hidden_ratio = 1. - visible_ratio
    root_length = hidden_ratio * length
 
    dir_vec = Vector3(pt1)-Vector3(pt0)
    d = dir_vec.normalize()
    pt2 = Vector3(pt1) + (root_length)*dir_vec
    # print(str(d+root_length)+ ' vs ' + str(length))
    return Polyline([pt0, pt1, pt2])

def curve2surface(crv, radius):
    # statis section
    p = [(0.5, 0), (0, 0.5), (-0.5, 0), (0, -0.5), (0.5, 0)]
    section = Polyline2D(p)

    n = len(crv)
    r = [(radius, radius) for i in range(n)]
    sweep = Extrusion(crv, section, Point2Array(r))
    return sweep

################################


def brace_roots(nb_whorl=2,
                whorl_heights=[2., 8.],
                nb_root=[16, 14],
                whorl_stem_radius=None,
                root_angle=[(110., 90.),(125., 90.)],
                root_length=[5., 19.],
                visible_ratio=[.5, .5],
                root_diameter=[3., 1.],
                root_stiffness= [600, 600]):
    """ Generate a set of brace roots in different whorls based on parameters or measurements.

    Args:
        nb_whorl: number of whorls
        whorl_heights: list of heights of each whorl
        nb_root: list of the number of roots per whorl
        root_angle:  base and top angle for each brace root
        visible_ratio: ratio of the length that is visible compared to the length in the soil.

    Returns: A dict with individual organ dimensions and geometric
    parameters needed by cereals generation

    """

    roots = {}

    roots['nb_whorl'] = nb_whorl
    if nb_whorl == 0:
        return roots
    
    # TODO ; check the validity
    roots['whorl_heights'] = whorl_heights
    roots['nb_root'] = nb_root

    if not isinstance(root_length[0], list):
        roots['root_length'] = [[root_length[i]]*nb_root[i] for i in range(nb_whorl)]
    else:
        roots['root_length'] = root_length

    if not isinstance(visible_ratio[0], list):
        roots['visible_ratio'] = [[visible_ratio[i]]*nb_root[i] for i in range(nb_whorl)]
    else:
        roots['visible_ratio'] = visible_ratio

    if not isinstance(root_diameter[0], list):
        roots['root_radius'] = [[root_diameter[i]/2.]*nb_root[i] for i in range(nb_whorl)]
    else:
        roots['root_radius'] = (np.array(root_diameter)/2.).tolist()

    if not isinstance(root_angle[0], list):
        roots['root_angle'] = [[root_angle[i]]*nb_root[i] for i in range(nb_whorl)]
    else:
        roots['root_angle'] = root_angle

    if not isinstance(root_stiffness[0], list):
        roots['root_stiffness'] = [[root_stiffness[i]]*nb_root[i] for i in range(nb_whorl)]
    else:
        roots['root_stiffness'] = root_stiffness

    # brace roots are packed around the node, so that stem perimeter = sum(root diameter)
    roots['whorl_stem_radius'] = whorl_stem_radius
    if whorl_stem_radius is None:
        roots['whorl_stem_radius'] = [np.sum(radii) / (2*np.pi) for radii in roots['root_radius']]
    return roots



def brace_root_polylines(brace_roots):
    """Compute brace root polylines of a braceroot whorl"""
    broots = brace_roots
    nb_whorl = broots['nb_whorl']
    lengths = broots['root_length']
    visible_ratios = broots['visible_ratio']
    whorl_stem_radius = broots['whorl_stem_radius']
    root_radius = broots['root_radius']
    curves, radius = [], []
    for i in range(nb_whorl):
        whs = broots['whorl_heights']
        height = whs[i]
        nb_root = broots['nb_root'][i]
        if nb_root:
            delta_angle = 360. / nb_root
            angle = 0.
            for j in range(nb_root):
                angles = (0.,0.) # TODO
                crv = brace_curve(height, lengths[i][j], visible_ratios[i][j],
                                  angles, whorl_stem_radius[i], phyllotaxis=angle)
                curves.append(crv)
                radius.append(root_radius[i][j])
                angle += delta_angle
    return curves, radius



def view3d(brace_roots, stem_height, stem=False, stalk_angle=0., stem_radius=0.03):
    """ Visualise the brace roots with or without the stem.
    
    """

    broots = brace_roots
    scene = Scene()

    whorl_stem_radius = broots.get('whorl_stem_radius', [stem_radius])
    if stem:
        stem_radius = max(whorl_stem_radius)
        geometry=Cylinder(stem_radius, stem_height)
        if stalk_angle:
            print('angle is ', stalk_angle)
            geometry = AxisRotated(
                axis=Vector3(1,0,0), 
                angle=stalk_angle, 
                geometry=geometry)
        _stem = Shape(geometry=geometry,
                      appearance=Material(Color3(10,200,10)))
        scene.add(_stem)

    if broots['nb_whorl'] == 0.:
        return scene

    curves, radius = brace_root_polylines(broots)
    for crv, r in zip(curves, radius):
        brsurface = Shape(geometry=curve2surface(crv, r),
                                  appearance=Material(Color3(200, 100,10)))
        scene.add(brsurface)

    return scene

##############################################################################
# Helper functions to create and test whorls 

def no_whorl():
    """ Test the geometry of the brace root model. 
    Here we test only one whorl. 
    """
    nb_whorl = 0
    br = brace_roots(nb_whorl=nb_whorl)
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
    br = brace_roots(
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

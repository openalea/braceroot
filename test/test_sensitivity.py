from math import cos, sin, degrees, radians
from itertools  import product

import numpy as np
from scipy.stats import linregress
import pandas as pd

from braceroot import brace_root, mechanic

from test_braceroot import no_whorl, whorls

##############################################################################
# Test if the model behave linearly % wind force
##############################################################################

def test_linearity_w0():
    # No whorl
    br0 = whorls(whorl=(0,0,0))
    angles = []
    winds = list(range(0,100,10))
    for wind in winds:
        a = mechanic.mechanics(br0, wind) 
        angles.append(a[0])

    regress = linregress(winds, angles)

    assert(regress.intercept_stderr<0.01)

def test_linearity_w1():
    # One whorl
    br1 = whorls(whorl=(1,0,0))
    angles = []
    winds = list(range(0,100,10))
    for wind in winds:
        a = mechanic.mechanics(br1, wind) 
        angles.append(a[0])

    regress = linregress(winds, angles)

    assert(regress.intercept_stderr<0.01)

def test_linearity_w2():
    # Two whorls
    br2 = whorls(whorl=(1,1,0))
    angles = []
    winds = list(range(0,100,10))
    for wind in winds:
        a = mechanic.mechanics(br2, wind) 
        angles.append(a[0])

    regress = linregress(winds, angles)

    assert(regress.intercept_stderr<0.01)

def test_linearity_w3():
    # Three whorls
    br3 = whorls(whorl=(1,1,1))
    angles = []
    winds = list(range(0,100,10))
    for wind in winds:
        a = mechanic.mechanics(br3, wind) 
        angles.append(a[0])

    regress = linregress(winds, angles)

    assert(regress.intercept_stderr<0.01)

##############################################################################
# Root mechanics
##############################################################################

def test_root_stiffness_mass():
    br0 = whorls(whorl=(0,0,0))
    angles = []
    wind_force=10
    stalk_stiffs = list(np.linspace(30,300,10))
    stem_weights = list(np.linspace(0.05,0.3,10))

    data = []
    for stiff, weight in product(stalk_stiffs, stem_weights):
        a = mechanic.mechanics(
            br0, wind_force=wind_force, 
            stem_mass=float(weight), 
            stalk_stiffness=float(stiff)) 
        angles.append(a[0])
        data.append((stiff, weight, degrees(a[0])))

    df = pd.DataFrame.from_records(
        data, 
        columns=['stalk_stiffness', 'stem_mass', 'angle']
        )
    return df

def test_root_stiffness_height():
    br0 = whorls(whorl=(0,0,0))

    wind_force=10
    stalk_stiffs = list(np.linspace(30,300,10))
    stem_mass = 0.2 #list(np.linspace(0.05,0.3,10))
    stem_heights = list(np.linspace(0.5,3.,10))

    data = []
    for stiff, height in product(stalk_stiffs, stem_heights):
        a = mechanic.mechanics(
            br0, wind_force=wind_force, 
            stem_mass=float(stem_mass),
            stem_height=float(height),
            stalk_stiffness=float(stiff)) 
        data.append((stiff, height*100, degrees(a[0])))

    df = pd.DataFrame.from_records(
        data, 
        columns=['stalk_stiffness', 'stem_height(cm)', 'angle']
        )
    return df


def plot_surface(df):
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt

    cols = df.columns
    X = cols[0]
    Y = cols[1]
    Z = cols[2]

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot_trisurf(df[X], df[Y], df[Z], 
                    cmap=plt.cm.viridis, linewidth=0.01)
    ax.set_xlabel(X)
    ax.set_ylabel(Y)
    ax.set_zlabel(Z)
    
    plt.show()

##############################################################################
# Whorl numbers
##############################################################################

def test_whorl_nb_root():
    ws = [(0,0,0),(1,0,0),(1,1,0),(1,1,1)]

    stiff = 100.
    height = 2.5 # before it was 2m
    stem_mass = 0.1
    wind_force = 10.

    data = []    
    for nb in range(2,20,2):
        for i, w in enumerate(ws):
            br = whorls(whorl=w, nb_root=nb)
            a = mechanic.mechanics(
                br, wind_force=wind_force, 
                stem_mass=float(stem_mass),
                stem_height=float(height),
                stalk_stiffness=float(stiff))            
            data.append((nb, i, degrees(a[0])))
    
    df = pd.DataFrame.from_records(
        data, 
        columns=['#roots per whorl', '#whorls', 'angle']
        )
    return df

##############################################################################
# Whorl parameters
##############################################################################

def test_whorl_param1():
    stiff = 100.
    height = 2.5 # before it was 2m
    stem_mass = 0.1
    wind_force = 10.    
    
    nb_whorl = 1
    nb_roots=5
    root_diameters = 0.03
    root_length = 0.15
    whorl_heights = np.linspace(0.01,0.08,10)
    root_angles = np.linspace(100, 170,10)
    root_stiffness=np.linspace(50,800, 10)
    
    # prodct between height, angle and stiffness
    # 1. height / angle 
    rstiff = 300.

    data = []
    for root_height, root_angle in product(whorl_heights, root_angles):
        rh = float(root_height)
        ra = float(root_angle)
        length = rh / cos(radians(180.-ra))
        visible_ratio = length/root_length
        br = brace_root.brace_roots(
            nb_whorl=nb_whorl,                      
            whorl_heights=[rh],
            nb_root=[nb_roots],
            root_angle=[ra],
            root_length=[root_length],
            visible_ratio=[visible_ratio],
            root_diameter= [root_diameters],
            root_stiffness=[rstiff]
            )
        a = mechanic.mechanics(
            br, wind_force=wind_force, 
            stem_mass=float(stem_mass),
            stem_height=float(height),
            stalk_stiffness=float(stiff))

        data.append((rh, 180.-ra, degrees(a[0])))
    
    df = pd.DataFrame.from_records(
        data, 
        columns=['root height', 'root angle', 'angle']
        )
    return df

def test_whorl_param2():
    stiff = 100.
    height = 2.5 # before it was 2m
    stem_mass = 0.1
    wind_force = 10.    
    
    nb_whorl = 1
    nb_roots=5
    root_diameters = 0.03
    root_length = 0.15
    whorl_heights = np.linspace(0.01,0.08,10)
    root_angles = np.linspace(100, 170,10)
    root_stiffness=np.linspace(50,800, 10)
    
    # prodct between height, angle and stiffness
    # 1. height / angle 
    rstiff = 300.
    rh = root_height = 0.04
    data = []
    for root_angle, rstiff in product(root_angles, root_stiffness):
        rstiff = float(rstiff)
        ra = float(root_angle)
        length = rh / cos(radians(180.-ra))
        visible_ratio = length/root_length
        br = brace_root.brace_roots(
            nb_whorl=nb_whorl,                      
            whorl_heights=[rh],
            nb_root=[nb_roots],
            root_angle=[ra],
            root_length=[root_length],
            visible_ratio=[visible_ratio],
            root_diameter= [root_diameters],
            root_stiffness=[rstiff]
            )
        a = mechanic.mechanics(
            br, wind_force=wind_force, 
            stem_mass=float(stem_mass),
            stem_height=float(height),
            stalk_stiffness=float(stiff))

        data.append((180-ra, rstiff, degrees(a[0])))
    
    df = pd.DataFrame.from_records(
        data, 
        columns=['root angle', 'root stiffness', 'angle']
        )
    return df

def test_whorl_param3():
    stiff = 100.
    height = 2.5 # before it was 2m
    stem_mass = 0.1
    wind_force = 10.    
    
    nb_whorl = 1
    nb_roots=5
    root_diameters = 0.03
    root_length = 0.15
    whorl_heights = np.linspace(0.01,0.08,10)
    root_angles = np.linspace(100, 170,10)
    root_stiffness=np.linspace(50,800, 10)
    
    # prodct between height, angle and stiffness
    # 1. height / angle 
    rstiff = 300.
    ra = root_angle = 180-45
    data = []

    for root_height, rstiff in product(whorl_heights, root_stiffness):
        rh = float(root_height)
        rstiff = float(rstiff)
        length = rh / cos(radians(180.-ra))
        visible_ratio = length/root_length
        br = brace_root.brace_roots(
            nb_whorl=nb_whorl,                      
            whorl_heights=[rh],
            nb_root=[nb_roots],
            root_angle=[ra],
            root_length=[root_length],
            visible_ratio=[visible_ratio],
            root_diameter= [root_diameters],
            root_stiffness=[rstiff]
            )
        a = mechanic.mechanics(
            br, wind_force=wind_force, 
            stem_mass=float(stem_mass),
            stem_height=float(height),
            stalk_stiffness=float(stiff))

        data.append((rh, rstiff, degrees(a[0])))
    
    df = pd.DataFrame.from_records(
        data, 
        columns=['root height', 'root stiffness', 'angle']
        )
    return df

from math import cos, sin, degrees, radians
import numpy as np
from scipy.stats import linregress

from braceroot import brace_root, mechanic

from test_braceroot import no_whorl, whorls


def test_linearity_w1():
    br1 = whorls(whorl=(1,0,0))
    angles = []
    winds = list(range(0,100,10))
    for wind in winds:
        a = mechanic.mechanics(br1, wind) 
        angles.append(a[0])

    regress = linregress(winds, angles)

    assert(regress.intercept_stderr<0.01)

def test_linearity_w2():
    br1 = whorls(whorl=(1,1,0))
    angles = []
    winds = list(range(0,100,10))
    for wind in winds:
        a = mechanic.mechanics(br1, wind) 
        angles.append(a[0])

    regress = linregress(winds, angles)

    assert(regress.intercept_stderr<0.01)

def test_linearity_w3():
    br1 = whorls(whorl=(1,1,1))
    angles = []
    winds = list(range(0,100,10))
    for wind in winds:
        a = mechanic.mechanics(br1, wind) 
        angles.append(a[0])

    regress = linregress(winds, angles)

    assert(regress.intercept_stderr<0.01)


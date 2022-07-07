""" Test the brace root object .
 three.
"""

from math import cos, sin, degrees, radians
import numpy as np
from braceroot import brace_root, mechanic


def test_br2_1():
    "Test Brace root 2 without 1 whorl"

    br2_1 = brace_root.whorls(whorl=(0,1,0))
    assert(len(br2_1['root_stiffness'][1])==10)
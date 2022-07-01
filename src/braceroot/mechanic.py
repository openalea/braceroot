""" Mechanical equilibrium of maize

"""

# Later on
#import sympy

from math import cos, sin, sqrt, degrees, radians, pi
from scipy import optimize
from openalea.plantgl.all import Vector3, norm


class Constant(object):
    g = 9.81

class MechanicalElement(object):
    """ Abstract base class for defining force and moment of each element on the system.
    """

    def set_angle(self, stem_theta):
        """ This is the unknown.
        Lodging angle of the plant under wind at equilibrium.
        """
        self.stem_theta = float(stem_theta)
        self.stem_phi = 0. #float(stem_phi)

        print("Theta = ", self.stem_theta)


    def vector_stem(self):
        """Vector of the stem.
        """
        cos_theta = cos(self.stem_theta)
        sin_theta = sin(self.stem_theta)
        cos_phi = cos(self.stem_phi)
        sin_phi = sin(self.stem_phi)
        vector = Vector3(sin_theta * cos_phi,
                       sin_theta * sin_phi, 
                       cos_theta)
        return vector

    def force(self):
        """ Force applied to the system (N).
        """
        pass

    def moment(self):
        """ Moment of the force on the origin (base of the plant) (unit: N.m)
        """
        pass


class BraceRoot(MechanicalElement):
    """ Brace Root.
    """
    def __init__(self, length, theta, psi, stiffness, height):
        #length /= 100.
        #height /= 100.
        theta = radians(theta)
        psi = radians(psi)
        self.length0 = length
        self.theta0 = theta
        self.psi = psi
        self.stiffness = stiffness
        self.h = height

        # d: Distance from the origin to the fixed point of the brace root in the soil.
        #self.d = length * sin(theta)
        #self.d = self.h * tan(theta)
        self.d = sqrt(self.length0**2 - self.h**2)


    @property
    def length(self):
        """
        Actual length of the brace root under deformation.
        """
        sin_theta = sin(self.stem_theta)
        cos_phi = cos(self.stem_phi)
        sin_phi = sin(self.stem_phi)
        cos_psi = cos(self.psi)
        sin_psi = sin(self.psi)
        self._length = sqrt(self.h**2 + self.d**2 -
                            2 * self.h * self.d * sin_theta * 
                            (cos_phi * cos_psi + sin_phi * sin_psi)
                            )
        return self._length

    def vector_u(self):
        """Vector of the brace root.
        """
        cos_theta = cos(self.stem_theta)
        sin_theta = sin(self.stem_theta)
        cos_phi = cos(self.stem_phi)
        sin_phi = sin(self.stem_phi)
        cos_psi = cos(self.psi)
        sin_psi = sin(self.psi)
        return Vector3(self.h * sin_theta * cos_phi - self.d * cos_psi,
                       self.h * sin_theta * sin_phi -  self.d * sin_psi, 
                       self.h * cos_theta) / self.length


    def force(self):
        """Force applied to the system (N).
        """
        force = -self.stiffness * (self.length - self.length0) * self.vector_u()
        #print 'Brace Force = ', force
        return force


    def moment(self):
        """ Moment of the force on the origin (base of the plant) (unit: N.m)
        """
        # TODO : Check the sign of the force
        moment = self.h * self.vector_stem() ^ self.force()
        #print 'Brace Moment = ', moment
        return moment
    


class Stalk(MechanicalElement):
    """ Stalk.
    """

    def __init__(self, stiffness):
        self.stiffness = stiffness

    def force(self):
        """ Force applied to the system (N).
        """
        pass

    def moment(self):
        """ Moment of the force on the origin (base of the plant) (unit: N.m)
        """
        cos_phi = cos(self.stem_phi)
        sin_phi = sin(self.stem_phi)
        # TODO: why negative sign ????
        moment = - self.stiffness * self.stem_theta * Vector3(-sin_phi, cos_phi, 0)
        print('Stalk Moment = ', moment)
        return moment


class Weight(MechanicalElement):
    """ Weight of the plant. """

    def __init__(self, mass, height):
        self.height = height
        self.mass = mass

    def force(self):
        """ Force applied to the system (N).
        """
        force = Vector3(0, 0, - self.mass * Constant.g)
        print('Weight Force = ', force)
        return force

    def moment(self):
        """ Moment of the force on the origin (base of the plant) (unit: N.m)
        """
        OG = self.height / 2.
        moment = OG * self.vector_stem() ^ self.force()
        print('Weight Moment = ', moment)
        return moment


class Wind(MechanicalElement):
    """ Wind.
    """

    def __init__(self, force, height):
        self.height = height
        self._force = force

    def force(self):
        """ Force applied to the system (N).
        """
        force = self._force
        print('Wind Force = ', force)
        return force

    def moment(self):
        """ Moment of the force on the origin (base of the plant) (unit: N.m)
        """
        OG = self.height / 2.
        moment = OG * self.vector_stem() ^ self.force()
        print('Wind Moment = ', moment)
        return moment


class Solver(dict):

    def solve(self):
        f = self.moment_theorem()
        solutions = optimize.root(f, x0=0.)
        # We should only allow the solution to be between [-pi/2, pi/2].
        return solutions.x

    def moment_theorem(self):
        """ Return a function of theta.
        """
        weight = self['weight']
        wind = self['wind']
        stalk = self['stalk']
        whorl0 = self.get('whorl0', [])
        whorl1 = self.get('whorl1', [])

        elts = [weight, wind, stalk]
        if whorl0:
            elts.extend(whorl0)
            if whorl1:
                elts.extend(whorl1)

        def sum_moment(angles):
            theta = angles
            for elt in elts:
                elt.set_angle(theta)

            #norm_x = abs(sum(elt.moment().x for elt in elts))
            #norm_z = abs(sum(elt.moment().z for elt in elts))
            return sum(elt.moment().y for elt in elts)

        return sum_moment

def mechanics(roots, wind_force,
             stem_height=1.,
             stem_mass=1.,
             stalk_stiffness=600,
             debug=False
             ):
    """ Compute the mechanical forces and moments applied to a maize plant with (or without) brace roots.

    Assumption: We consider that the wind is a constant force.

    Inputs:
        - architecture (roots)
          - stem_height (m)
          - stem_mass (kg)
          - stalk_stiffness (N/m)
        - Wind force (N)

    Outputs:
        - Updated geometry
        - inclination angle(s)

    Algorithm:
        - decode the roots architecture
        - create the set of elements that define the mechanical system
        - solve the system
            - write the moment balance (weight_force)
            - get the final angle
        - visualise the resulting scene
    """
    broots = roots

    scene = Solver() # list of mecha elts


    # Stalk (aka stem) creation
    if 'whorl_stem_radius' in broots:
        whorl_stem_radius = broots['whorl_stem_radius']
        stem_radius = max(whorl_stem_radius)
        
    stalk = Stalk(stiffness=stalk_stiffness)

    scene['stalk'] = stalk

    # Weight
    weight = Weight(height=stem_height,
                    mass=stem_mass)
    scene['weight'] = weight

    # Wind
    wind_force = Vector3(wind_force, 0, 0)
    wind = Wind(height=stem_height,
                force=wind_force)
    scene['wind'] = wind

    # Brace roots creation
    nb_whorl = broots['nb_whorl']
    if nb_whorl:
        lengths = broots['root_length'] #m
        visible_ratios = broots['visible_ratio']
        # root_angle has to be recomputed
        root_radius = broots['root_radius'] #m
        root_angle = broots['root_angle'] #degrees
        root_stiffness = broots['root_stiffness'] #N/m
        whs = broots['whorl_heights'] #m
        for i in range(nb_whorl):
            height = whs[i]
            nb_root = broots['nb_root'][i]

            if nb_root:
                delta_angle = 360. / nb_root
                angle = 0.
                for j in range(nb_root):
                    angles = (0.,0.) # TODO
                    angle += delta_angle

                    root = BraceRoot(length=lengths[i][j]*visible_ratios[i][j],
                                    theta=root_angle[i][j], psi=angle,
                                    stiffness=root_stiffness[i][j], height=height)
                    scene.setdefault('whorl'+str(i), []).append(root)

    final_theta = scene.solve()
    print("Final theta is ", degrees(final_theta), "degrees.")
    if debug:
        return final_theta[0], scene
    
    return final_theta[0]

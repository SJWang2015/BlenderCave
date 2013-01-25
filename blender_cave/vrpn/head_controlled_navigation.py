## Copyright © LIMSI-CNRS (2011)
##
## contributor(s) : Jorge Gascon, Damien Touraine, David Poirier-Quinot,
## Laurent Pointal, Julian Adenauer, 
## 
## This software is a computer program whose purpose is to distribute
## blender to render on CAVE(TM) device systems.
## 
## This software is governed by the CeCILL  license under French law and
## abiding by the rules of distribution of free software.  You can  use, 
## modify and/ or redistribute the software under the terms of the CeCILL
## license as circulated by CEA, CNRS and INRIA at the following URL
## "http://www.cecill.info". 
## 
## As a counterpart to the access to the source code and  rights to copy,
## modify and redistribute granted by the license, users are provided only
## with a limited warranty  and the software's author,  the holder of the
## economic rights,  and the successive licensors  have only  limited
## liability. 
## 
## In this respect, the user's attention is drawn to the risks associated
## with loading,  using,  modifying and/or developing or reproducing the
## software by the user in light of its specific status of free software,
## that may mean  that it is complicated to manipulate,  and  that  also
## therefore means  that it is reserved for developers  and  experienced
## professionals having in-depth computer knowledge. Users are therefore
## encouraged to load and test the software's suitability as regards their
## requirements in conditions enabling the security of their systems and/or 
## data to be ensured and,  more generally, to use and operate it in the 
## same conditions as regards security. 
## 
## The fact that you are presently reading this means that you have had
## knowledge of the CeCILL license and that you accept its terms.
## 

import mathutils
import math
import blender_cave.base
from blender_cave import user

class _HCNav(blender_cave.base.Base):
    def __init__(self, parent, element):
        super(_HCNav, self).__init__(parent)
        self._element = element
        self.reset()
        self._positionFactors    = [{}, {}, {}]
        self._orientationFactors = {}
        self._headNeckLocation   = mathutils.Matrix.Translation((0.0, -0.15, 0.12))

        # Default factors
        self.setPositionFactors(0, 0.5, 3)
        self.setPositionFactors(1, 0.5, 3)
        self.setPositionFactors(2, 0.5, 3)
        self.setOrientationFactors(0.07, 2)

    def reset(self):
        self._position             = mathutils.Vector((0.0, 0.0, 0.0))
        self._quaternion           = mathutils.Quaternion()
        self._orientation          = mathutils.Matrix()
        self._orientation_inverted = mathutils.Matrix()
        self._calibrate            = False
        self._run                  = False
        self._calibrated           = False

    def setPositionFactors(self, component, attenuation, power, max = 1.0): # should be a vector
        self._positionFactors[component]['attenuation'] = attenuation
        self._positionFactors[component]['power'] = power
        self._positionFactors[component]['max'] = max

    def setOrientationFactors(self, attenuation, power, max = 1.0): # should be a vector
        self._orientationFactors['attenuation'] = attenuation
        self._orientationFactors['power'] = power
        self._orientationFactors['max'] = max

    def setHeadNeckLocation(self, location): 
        self._headNeckLocation = location

    def calibration(self):
        self._calibrate = True

    def update(self, newState):
        if newState == HCNav.CALIBRATE:
            self._calibrate = True
        elif newState == HCNav.START:
            if self._calibrated:
                self._run = True
            else:
                self.getLogger().warning('cannot start while not calibrated !')
        elif newState == HCNav.STOP:
            self._run = False
        elif newState == HCNav.TOGGLE:
            if self._run:
                self._run = False
            else:
                if self._calibrated:
                    self._run = True
                else:
                    self.getLogger().warning('cannot start while not calibrated !')
        elif newState == HCNav.RESET:
            self.reset()

    def setHeadLocation(self, matrix):
        matrix =  matrix * self._headNeckLocation
        if self._calibrate:
            self._position             = matrix.to_translation()
            self._quaternion           = matrix.to_quaternion()
            self._orientation          = matrix.to_3x3()
            self._orientation_inverted = self._orientation_inverted.inverted()
            self._calibrate            = False
            self._calibrated           = True

        if not self._run:
            return

        position = (self._position - matrix.to_translation())
        for i in range(0,3):
            scalePosition = position[i]
            if (scalePosition < 0):
                scalePosition *= -1
            scalePosition *= self._positionFactors[i]['attenuation']
            scalePosition = math.pow(scalePosition, self._positionFactors[i]['power'])
            if scalePosition > self._positionFactors[i]['max']:
                scalePosition = self._positionFactors[i]['max'] 
            position[i] *= scalePosition

        quat_o = self._quaternion
        quat_d = matrix.to_quaternion()

        scaleOrientation = quat_o.slerp(quat_d, 1).angle
        scaleOrientation *= self._orientationFactors['attenuation']
        scaleOrientation = math.pow(scaleOrientation, self._orientationFactors['power'])
        if scaleOrientation > self._orientationFactors['max']:
            scaleOrientation = self._orientationFactors['max']
        orientation = quat_o.slerp(quat_d, scaleOrientation)

        orientation = self._orientation * orientation.to_matrix().inverted()

        delta = orientation.to_4x4() * mathutils.Matrix.Translation(position)

        if isinstance(self._element, user.User):
            self._element.setVehiclePosition(delta * self._element.getVehiclePosition())
        else:
            self._element(delta)

class HCNav(blender_cave.base.Base):
    CALIBRATE = 'calibrate'
    START     = 'start'
    STOP      = 'stop'
    TOGGLE    = 'toggle'
    RESET     = 'reset'

    def __init__(self, parent, method = None):
        super(HCNav, self).__init__(parent)

        if method is None:
            for user in self.getBlenderCave().getAllUsers():
                user._HCNav = _HCNav(self, user)
        elif hasattr(method, '__call__'):
            self._local = _HCNav(self, method)

    def setPositionFactors(self, component, attenuation, power, max = 1.0, user = None): # should be a vector
        if hasattr(self, '_local'):
            self._local.setPositionFactors(component, attenuation, power, max)
            return
        if user is None:
            for user in self.getBlenderCave().getAllUsers():
                user._HCNav.setPositionFactors(component, attenuation, power, max)
        else:
            user._HCNav.setPositionFactors(component, attenuation, power, max)

    def setOrientationFactors(self, attenuation, power, max = 1.0, user = None): # should be a vector
        if hasattr(self, '_local'):
            self._local.setOrientationFactors(attenuation, power, max)
            return
        if user is None:
            for user in self.getBlenderCave().getAllUsers():
                user._HCNav.setOrientationFactors(attenuation, power, max)
        else:
            user._HCNav.setOrientationFactors(attenuation, power, max)

    def setHeadNeckLocation(self, user, location): 
        if hasattr(self, '_local'):
            self._local.setHeadNeckLocation(location)
            return
        user._HCNav.setHeadNeckLocation(location)
       
    def update(self, state, user = None):
        if hasattr(self, '_local'):
            self._local.update(state)
            return
        if user is None:
            for user in self.getBlenderCave().getAllUsers():
                user._HCNav.update(state)
        else:
            user._HCNav.update(state)

    def setHeadLocation(self, user, info):
        if hasattr(self, '_local'):
            self._local.setHeadLocation(info['matrix'])
            return
        user._HCNav.setHeadLocation(info['matrix'])

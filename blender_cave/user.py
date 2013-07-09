# -*- coding: iso-8859-1 -*-
## Copyright � LIMSI-CNRS (2013)
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
import blender_cave.base
import blender_cave.buffer

class User(blender_cave.base.Base):

    SYNCHRONIZER_COMMAND_USER_POSITION    = b'u'
    SYNCHRONIZER_COMMAND_VEHICLE_POSITION = b'v'

    def __init__(self, parent, id, config):
        super(User, self).__init__(parent)

        self._id               = id
        self._name             = config['name']
        self._eye_separation   = config['eye_separation']
        self._default_position = mathutils.Matrix.Translation((config['default_position']))

        self._position         = self._default_position
        self._vehicle_position = mathutils.Matrix()

        self._previous         = { 'user_position': 0,
                                   'vehicle_position': 0 }

        self.getBlenderCave().addObjectToSynchronize(self, 'userSynchronization-' + self._name)

    def getID(self):
        return self._id
        
    def getName(self):
        return self._name
        
    def getPosition(self):
        return self. _position

    def getVehiclePosition(self):
        return self._vehicle_position

    def getEyeSeparation(self):
        return self._eye_separation

    def setPosition(self, position):
        self._position = position

    def setVehiclePosition(self, position):
        self._vehicle_position = position

    def resetVehiclePosition(self):
        self._vehicle_position = mathutils.Matrix()

    # Both methods are use for the synchronization mechanism ...
    def getSynchronizerBuffer(self):
        buffer = blender_cave.buffer.Buffer()

        if (self._previous['user_position'] != self.getPosition()):
            self._previous['user_position'] = self.getPosition()
            buffer.command(self.SYNCHRONIZER_COMMAND_USER_POSITION)
            buffer.matrix_4x4(self.getPosition())

        if (self._previous['vehicle_position'] != self.getVehiclePosition()):
            self._previous['vehicle_position'] = self.getVehiclePosition()
            buffer.command(self.SYNCHRONIZER_COMMAND_VEHICLE_POSITION)
            buffer.matrix_4x4(self.getVehiclePosition())

        return buffer

    def processSynchronizerBuffer(self, buffer):
        while not buffer.isEmpty():
            command = buffer.command()

            if (command == self.SYNCHRONIZER_COMMAND_USER_POSITION):
                self.setPosition(buffer.matrix_4x4())

            elif (command == self.SYNCHRONIZER_COMMAND_VEHICLE_POSITION):
                self.setVehiclePosition(buffer.matrix_4x4())

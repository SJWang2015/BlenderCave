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

from . import base
import bge
import mathutils
import blender_cave.exceptions

class Object(base.Base):
    def __init__(self, parent, obj, configuration):
        super(Object, self).__init__(parent, 'object', len(parent._objects) + 1)
        if isinstance(obj, str):
            self._object = bge.logic.getCurrentScene().objects[obj]
        elif isinstance(obj, bge.types.KX_GameObject):
            self._object = obj
        else:
            raise blender_cave.exceptions.OSC_Invalid_Object(str(obj))
        if 'BlenderCave_OSC' in self._object:
            raise blender_cave.exceptions.OSC_Invalid_Already_Created(str(obj))
        self._configuration = configuration
        self._commands['sound']    = { 'type'  : 'string'}
        self._commands['position'] = { 'type'  : 'matrix'}
        self._commands['loop']     = { 'type'  : 'state'}
        self._commands_order       = ['sound', 'loop', 'volume', 'start', 'position', 'mute']
        self.define_commands()

        if 'sound' in configuration:
            self.sound(configuration['sound'])
        self._object['BlenderCave_OSC'] = self

    def run(self):
        camera = bge.logic.getCurrentScene().active_camera
        camera_position = camera.worldOrientation.to_4x4() * mathutils.Matrix.Translation(camera.worldPosition)
        object_position = self._object.worldOrientation.to_4x4() * mathutils.Matrix.Translation(self._object.worldPosition)
        self.position(camera_position.inverted() * object_position)
        super(Object, self).run()

    def getName(self):
        return self._object.name

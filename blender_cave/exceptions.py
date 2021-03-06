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

class Common (Exception):
    def __init__(self, reason):
        self._reason = reason

    def __str__(self):
        return self._reason

class Main (Common):
    def __init__(self, reason):
        super(Main, self).__init__(reason)

class Environment (Common):
    def __init__(self, reason):
        super(Environment, self).__init__(reason)

class Configure (Common):
    def __init__(self, reason):
        super(Configure, self).__init__(reason)

class Synchronizer (Common):
    def __init__(self, reason):
        super(Synchronizer, self).__init__(reason)

class Broadcaster (Common):
    def __init__(self, reason):
        super(Broadcaster, self).__init__(reason)

class Controller (Common):
    def __init__(self, reason):
        super(Controller, self).__init__(reason)

class Connector (Common):
    def __init__(self, state, reason):
        super(Connector, self).__init__(reason)
        self._state = state

    def getState(self):
        return self._state

class Quit (Common):
    def __init__(self, reason):
        super(Quit, self).__init__(reason)

class User (Common):
    def __init__(self, reason):
        super(User, self).__init__(reason)

class VirtualEnvironment (Common):
    def __init__(self, reason):
        super(VirtualEnvironment, self).__init__(reason)

class VRPN (Common):
    def __init__(self, reason):
        super(VRPN, self).__init__(reason)

class Processor_Invalid_Device(Common):
    def __init__(self, reason):
        super(Processor_Invalid_Device, self).__init__(reason)

class OSC_Invalid_Type(Common):
    def __init__(self, reason):
        super(OSC_Invalid_Type, self).__init__(reason)

class OSC_Invalid_Object(Common):
    def __init__(self, reason):
        super(OSC_Invalid_Object, self).__init__(reason)

class OSC_Invalid_Already_Created(Common):
    def __init__(self, reason):
        super(OSC_Invalid_Already_Created, self).__init__(reason)

class Reload(Common):
    def __init__(self, reason):
        super(Reload, self).__init__(reason)

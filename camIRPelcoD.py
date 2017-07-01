#-*-coding:Utf-8 -*

"""
    Copyright (C) 2017 Cazé-François Guillaume

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


This module is used to create and send commands from the computer to a DTRX3 receiver.

The only functions user has to activate are located in the "camera" class. This can be done by
creating a camera object (see Example section of this docstring).
The functions in the two other classes have to be used only by the program itself.

Classes
-------
pelco_options : bytes 3 and 4 of the command

message : the full message, including synch byte and checksum

camera : the camera object
	User has to define receiver address and serial port
	
Example
-------
from cmdPelcoD2 import *

my_camera = camera(port_id, receiver_address)

#make tourelle pan left
my_camera.left()
#stop rotation
my_camera.stop()
"""

#External library pyserial
#
#https://pythonhosted.org/pyserial/
import serial

class pelco_options(object):
    """
    This class creates bytes 3 and 4 of the command
    
    Attributes
    ----------
    Every attribute is a bit from bytes 3 and 4.
    Please refer to the Pelco D Protocol documentation for more details.
    
    Functions
    ---------
    The attributes are private.
    The functions are used to define/read attributes with :
    	get_attribute
    	set_attribute
    	property
    """
    def __init__(self):
        """	
        Setup all bits to 0
        """
		
        self.__sense = 0
        self.__toggle_automan = 0
        self.__toggle_onoff = 0
        self.__iris_close = 0
        self.__iris_open = 0
        self.__focus_near = 0
        self.__focus_far = 0
        self.__zoom_wide = 0
        self.__zoom_tele = 0
        self.__tilt_down = 0
        self.__tilt_up = 0
        self.__pan_left = 0
        self.__pan_right = 0
        self.__preset = 0
        
        
    def get_sense(self):
        return self.__sense
    def set_sense(self, sense):
        self.__sense = sense
    sense = property(get_sense, set_sense)
    
    def get_toggle_automan(self):
        return self.__toggle_automan
    def set_toggle_automan(self, toggle_automan):
        self.__toggle_automan = toggle_automan
    toggle_automan = property(get_toggle_automan, set_toggle_automan)

    def get_toggle_onoff(self):
        return self.__toggle_onoff
    def set_toggle_onoff(self, toggle_onoff):
        self.__toggle_onoff = toggle_onoff
    toggle_onoff = property(get_toggle_onoff, set_toggle_onoff)
    
    def get_iris_close(self):
        return self.__iris_close
    def set_iris_close(self, iris_close):
        self.__iris_close = iris_close
    iris_close = property(get_iris_close, set_iris_close)
    
    def get_iris_open(self):
        return self.__iris_open
    def set_iris_open(self, iris_open):
        self.__iris_open = iris_open
    iris_open = property(get_iris_open, set_iris_open)
    
    def get_focus_near(self):
        return self.__focus_near
    def set_focus_near(self, focus_near):
        self.__focus_near = focus_near
    focus_near = property(get_focus_near, set_focus_near)
    
    def get_focus_far(self):
        return self.__focus_far
    def set_focus_far(self, focus_far):
        self.__focus_far = focus_far
    focus_far = property(get_focus_far, set_focus_far)
    
    def get_zoom_wide(self):
        return self.__zoom_wide
    def set_zoom_wide(self, zoom_wide):
        self.__zoom_wide = zoom_wide
    zoom_wide = property(get_zoom_wide, set_zoom_wide)
    
    def get_zoom_tele(self):
        return self.__zoom_tele
    def set_zoom_tele(self, zoom_tele):
        self.__zoom_tele = zoom_tele
    zoom_tele = property(get_zoom_tele, set_zoom_tele)
    
    def get_tilt_down(self):
        return self.__tilt_down
    def set_tilt_down(self, tilt_down):
        self.__tilt_down = tilt_down
    tilt_down = property(get_tilt_down, set_tilt_down)
    
    def get_tilt_up(self):
        return self.__tilt_up
    def set_tilt_up(self, tilt_up):
        self.__tilt_up = tilt_up
    tilt_up = property(get_tilt_up, set_tilt_up)
    
    def get_pan_left(self):
        return self.__pan_left
    def set_pan_left(self, pan_left):
        self.__pan_left = pan_left
    pan_left = property(get_pan_left, set_pan_left)
    
    def get_pan_right(self):
        return self.__pan_right
    def set_pan_right(self, pan_right):
        self.__pan_right = pan_right
    pan_right = property(get_pan_right, set_pan_right)

    def get_preset(self):
        return self.__preset
    def set_preset(self, preset):
        self.__preset = preset
    preset = property(get_preset, set_preset)


class message():
    """
    7-bytes Pelco D command.
    
    Functions
    ---------
    pelcod : creates the Pelco D command
    """
    def __init__(self):
        self.msg = []

    def pelcod(self, camera, camera_options, data1, data2):
        """
        Creates the Pelco D command by assembling the 7-bytes in the "msg" list.
        
        Parameters
        ----------
        camera : receiver address
        
        camera_options : bytes 3 and 4 (pelco_options object)
        
        data1 : byte 5
        	 - for a manual pilotage : pan speed
        	 - for a preset pilotage : always 0
        
        data2 : byte 6
        	 - for a manual pilotage : tilt speed
        	 - for a preset pilotage : preset number
        
        Returns
        -------
        msg (type=list) : the 7-bytes command to be sent, including synch byte and checksum
        """

        command1 = 0
        command1 += camera_options.sense*128
        command1 += 0*64
        command1 += 0*32
        command1 += camera_options.toggle_automan*16
        command1 += camera_options.toggle_onoff*8
        command1 += camera_options.iris_close*4
        command1 += camera_options.iris_open*2
        command1 += camera_options.focus_near*1
    
        command2 = 0
        command2 += camera_options.focus_far*128
        command2 += camera_options.zoom_wide*64
        command2 += camera_options.zoom_tele*32
        command2 += camera_options.tilt_down*16
        command2 += camera_options.tilt_up*8
        command2 += camera_options.pan_left*4
        command2 += camera_options.pan_right*2
        command2 += camera_options.preset*1
   
        checksum = (camera + command1 + command2 + data1 + data2) % 256
        msg = [0xFF, camera, command1, command2, data1, data2, checksum]
        return msg 

class camera():
    """
    Camera defined by the receiver address and the serial port.
    
    WARNING : once activated, all of the moves described down there will be performed until
    the stop function is used, except for preset functions.
    """
    def __init__(self, port_id, addr):
        self.port_id = port_id
        self.addr = addr
        self.device_found = False
        self.command = message()
        self.action = pelco_options()
        self.data1 = 0
        self.data2 = 0

    def left(self):
        """
        Makes tourelle pan to the left
        """
        self.action.pan_left = 1
        self.data1 = 0x3F
        self.data2 = 0
        self.send(self.command.pelcod(self.addr, self.action, self.data1, self.data2), self.port_id)
        self.action = pelco_options()

    def right(self):
        """
        Makes tourelle pan to the right
        """
        self.action.pan_right = 1
        self.data1 = 0x3F
        self.data2 = 0
        self.send(self.command.pelcod(self.addr, self.action, self.data1, self.data2), self.port_id)
        self.action = pelco_options()

    def up(self):
        """
        Makes tourelle tilt up
        """
        self.action.tilt_up = 1
        self.data1 = 0
        self.data2 = 0x3F
        self.send(self.command.pelcod(self.addr, self.action, self.data1, self.data2), self.port_id)
        self.action = pelco_options()

    def down(self):
        """
        Makes tourelle tilt down
        """
        self.action.tilt_down = 1
        self.data1 = 0
        self.data2 = 0x3F
        self.send(self.command.pelcod(self.addr, self.action, self.data1, self.data2), self.port_id)
        self.action = pelco_options()

    def setPreset(self, number):
        """
        Save the current position as preset n° number.
        
    	You can chose numbers between 2 and 40.
    	Preset n°1 is reserved for the start position.
    	"""
        self.action.pan_right = 1
        self.action.preset = 1
        self.data1 = 0
        self.data2 = number
        self.send(self.command.pelcod(self.addr, self.action, self.data1, self.data2), self.port_id)
        self.action = pelco_options()

    def goToPreset(self, number):
        """
        Move the tourelle to the position saved for preset n°number
        """
        self.action.pan_left = 1
        self.action.pan_right = 1
        self.action.preset = 1
        self.data1 = 0
        self.data2 = number
        self.send(self.command.pelcod(self.addr, self.action, self.data1, self.data2), self.port_id)
        self.action = pelco_options()

    def clearPreset(self, number):
        """
        Clear the position saved for preset n°number.
    	
    	You should not delete preset n°1.
    	"""
        self.action.pan_left = 1
        self.action.preset = 1
        self.data1 = 0
        self.data2 = number
        self.send(self.command.pelcod(self.addr, self.action, self.data1, self.data2), self.port_id)
        self.action = pelco_options()

    def stop(self):
        """
        Interrupt current move of the tourelle
        """
        self.send([0xFF, 0x01, 0x00, 0x00, 0x00, 0x00, 0x01], self.port_id)
        self.action = pelco_options()

    def send(self, message, port_id):
        """
        Sends a command from the computer to the receiver

        Using the pyserial library, checks if "port_serie" is open,
        and sends "message" to it.

        Parameters
        ----------
        message (type=list) : 7-bytes long Pelco D command

        port_id : name of the serial port on which receiver is connected
        """
        with serial.Serial(port_id, 9600, timeout=1) as port_serie:
            if port_serie.isOpen():
                port_serie.write(message)

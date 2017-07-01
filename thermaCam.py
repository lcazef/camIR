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


This module is used to communicate with a FLIR ThermoVision A40M camera through a serial port.
User has to create a thermacam object and to precise on which port the device is connected.

Classes
-------
thermacam : the thermal camera

imageStocker : the class used to build jpeg image file from buffer
"""

import serial
import os
import sys
import time

class thermacam():
  """
  This class establishes connection with the camera through serial port "port".
  
  Attributes
  ----------
  self.port : serial port on which the camera is connected
  
  self.baudrate : speed of the connection in bauds
  
  self.timeout : timeout, must be > 0
  
  self.uart : object used by serial lib
  
  self.answ : answer of the camera to a command
  
  Functions
  ---------
  openTest : checks if serial port is open
  
  writeCmd(command) : write specified command to buffer
  
  errors : checks if the command is correct or not, and if the answer is correct UTF-8
  
  maxSpeed : used when the object is created to set communication speed to 115200 bauds
  
  getImage(imageName) : transfer an image file from camera memory to the computer
  
  getSize(imageName) : used by getImage to get the size of the image to be transfered
  
  saveImage(imageName) : takes a photo of the current image and stores it in camera memory
  
  autofocus : autofocus
  
  focus : focus near, far or stop
  
  zoom(zoomPower) : makes the camera zoom. The value is a float between 1 and 8
  
  autoAdj(on | off) : enables/unables auto temperature adjust
  
  setRange(low, high) : sets temperature range
  """
  
  def __init__(self, port):
    self.port = port
    self.baudrate = 19200
    self.timeout = 0.1
    self.uart = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
    self.maxSpeed()
    self.answ = ""
  
  def openTest(self):
    if self.uart.isOpen():
      pass
    else:
      self.uart.open()
    
  def writeCmd(self, message):
    self.message = '\r' + message + '\r'
    self.openTest()
    self.uart.write(self.message.encode('utf-8'))
    self.answ = self.uart.readall()
    self.errors(self.answ)
    self.uart.close()

  def errors(self, answ):
    try:
      answ = answ.decode('utf-8')
      if answ.find("Error") == -1:
        print(answ)
      else:
        print("Error\n")
        print(answ)
    except UnicodeDecodeError:
      print("Not UTF-8\n")
      print(answ)
            
  def maxSpeed(self):
    self.writeCmd("baudrate -p 1 115200")
    self.baudrate = 115200
    self.uart.setBaudrate(115200)

  def getImage(self, imageName):
    self.imageName = imageName
    self.imgSize = self.getSize()
    self.stock = imageStocker(self.imgSize, self.uart, self.imageName)
    self.stock.buildStocker()
    self.stock.buildJPG()

  def getSize(self):
    self.openTest()
    self.uart.write('\rcd \images\r'.encode('utf-8'))
    self.uart.write('\rls -l\r'.encode('utf-8'))
    line = self.uart.readall().decode('utf-8')
    end = line.find(self.imageName) - 19
    line = line[:end]
    begin = end - 6
    line = line[begin:]
    size = int(line)
    self.uart.close()

    return(size)
  
  def saveImage(self, name):
    self.writeCmd('cd \images')
    message = 'store -j ' + name
    self.writeCmd(message)
    
  def autofocus(self):
    self.writeCmd('autofocus now')
  
  def focusInf(self):
    message = 'focus -i 25'
    self.writeCmd(message)
    
  def focusClose(self):
    message = 'focus -c 25'
    self.writeCmd(message)
    
  def focusStop(self):
    message = 'focus -s'
    self.writeCmd(message)
    
  def zoom(self, zoomPower):
    message = 'zoom ' + str(zoomPower)
    self.writeCmd(message)
    
  def setRange(self, tempLow, tempHigh):
    mediane = 'levelt ' + str((tempLow + tempHigh) / 2 + 273.15)
    intervalle = 'spant ' + str(tempHigh - tempLow)
    self.writeCmd("autoadj off")
    time.sleep(0.1)
    self.writeCmd(mediane)
    time.sleep(0.1)
    self.writeCmd(intervalle)
    
  def autoAdj(self, onOrOff):
    message = 'autoadj ' + onOrOff
    self.writeCmd(message)


class imageStocker():
  """
  This class stores blocks of 1024 bytes from buffer in order to create an image file.
  
  Attributes
  ----------
  self.size : size of the image to be transfered
  
  self.uart : object used by serial lib
  
  self.name : name of the image to be transfered
  
  self.stocker : bytes object in which the bytes blocks are stored
  
  Functions
  ---------
  buildStocker : gets and stores each block of the image
  
  buildJPG : dumps stocker into a jpeg file
  """
  def __init__(self, size, uart, name):
    self.size = size
    self.uart = uart
    self.name = name
    self.stocker = b''
    self.progressCounter = 0

  def buildStocker(self):
    blockNumber = 0
    j = 0
    part = b''
    reste = self.size % 1024    
    if self.uart.isOpen():
      pass
    else:
      self.uart.open()
    
    while blockNumber  < (self.size - reste):
      j = 0 
      message = "\rgetfblock \"\images\\" + self.name + "\" " + str(blockNumber) + " 1024 \r"
      print(message)
      self.uart.write(message.encode('utf-8'))
      time.sleep(0.1)
      part = self.uart.readall()
      while part[j] != 0x00:
        j += 1
      j += 3

      self.stocker += part[j:(1024+j)]
      self.progressCounter = 100 * (blockNumber / self.size)
      blockNumber += 1024
      
      
    
    j = 0
    message = "\rgetfblock \"\images\\" + self.name + "\" " + str(blockNumber) + ' ' + str(reste) + " \r"
    self.uart.write(message.encode('utf-8'))
    time.sleep(0.1)
    part = self.uart.readall()
    while part[j] != 0x00:
      j += 1
    j += 3
    self.stocker += part[j:(reste+j)]
    self.progressCounter = 100
    print(message)
    print(sys.getsizeof(self.stocker))
    self.uart.close()

  def buildJPG(self):
    with open(self.name, 'wb') as JPGFile:
      JPGFile.write(self.stocker)


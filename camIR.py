# -*- coding: utf-8 -*-

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
    

This module runs the camIR GUI.

User does not have to modify the code of this module.
Please do the setup and control of the tourelle using the GUI.

Classes
-------
camIRMain : inherits from the "QtGui.QMainWindow" and from "camIRGui.ui".
Defines the signals linked to buttons and keyboard events for main window of the program.
"""

from PyQt4 import QtGui, QtCore, uic
import sys
import camIRPelcoD
import thermaCam

class camIRMain(QtGui.QMainWindow):
    """
    Creates the main window.
       
    Attributes
    ----------
    keyPressEvent : redirects the "pressed" key events to the "newOnkeyPressEvent" method.
     
    keyReleaseEvent : same for the "released" key events.
    
    
    Methods
    -------
    buttonsDefinition : links the signals of the buttons to Pelco D functions.
    
    initCamera : uses the camIRPelcoD module to create a camera object.
    
    sendPreset : uses the camIRPelcoD module to set/go to/clear presets.
    
    newOnkeyPressEvent : uses the keyboard "pressed" events to control the tourelle.
    
    newOnkeyReleaseEvent : sends a "stop" message when a key is released.
    """
    def __init__(self):
        super(camIRMain, self).__init__()
        #Loading GUI from .ui file
        uic.loadUi("camIRGui.ui", self)
        #Redirecting key events
        self.keyPressEvent = self.newOnkeyPressEvent
        self.keyReleaseEvent = self.newOnkeyReleaseEvent
        #Using buttons signals
        #Cam infos validation
        QtCore.QObject.connect(self.CameraValida, QtCore.SIGNAL(("pressed()")), self.initCamera)
        QtCore.QObject.connect(self.thermacamValida, QtCore.SIGNAL(("pressed()")), self.initThermaCam)
    
    def buttonsDefinition(self):
        QtCore.QObject.connect(self.btnLeft, QtCore.SIGNAL(("pressed()")), self.camera1.left)
        QtCore.QObject.connect(self.btnLeft, QtCore.SIGNAL(("released()")), self.camera1.stop)       
        QtCore.QObject.connect(self.btnRight, QtCore.SIGNAL(("pressed()")), self.camera1.right)
        QtCore.QObject.connect(self.btnRight, QtCore.SIGNAL(("released()")), self.camera1.stop)
        QtCore.QObject.connect(self.btnUp, QtCore.SIGNAL(("pressed()")), self.camera1.up)
        QtCore.QObject.connect(self.btnUp, QtCore.SIGNAL(("released()")), self.camera1.stop)
        QtCore.QObject.connect(self.btnDown, QtCore.SIGNAL(("pressed()")), self.camera1.down)
        QtCore.QObject.connect(self.btnDown, QtCore.SIGNAL(("released()")), self.camera1.stop)
        #Preset validation
        QtCore.QObject.connect(self.ValidPreset, QtCore.SIGNAL(("pressed()")), self.sendPreset)
        
    def thermaBtnDefinition(self):
        QtCore.QObject.connect(self.btnFocusInf, QtCore.SIGNAL(("pressed()")), self.a40.focusInf)
        QtCore.QObject.connect(self.btnFocusInf, QtCore.SIGNAL(("released()")), self.a40.focusStop)
        QtCore.QObject.connect(self.btnFocusClose, QtCore.SIGNAL(("pressed()")), self.a40.focusClose)
        QtCore.QObject.connect(self.btnFocusClose, QtCore.SIGNAL(("released()")), self.a40.focusStop)
        self.btnFocusZoom.clicked.connect(self.a40.autofocus)
        
        #zoom
        self.btnZoom.clicked.connect(self.zoom)
        #range
        self.setRange.clicked.connect(self.rangeTemp)
        self.autoRange.clicked.connect(self.rangeTempAuto)
        #image
        self.imgAction.clicked.connect(self.doImgAction)
        
        
    def initCamera(self):
        serial_port = str(self.SerialList.currentText())
        print(serial_port)
        receiver_address = int(self.AddrList.value())
        self.camera1 = camIRPelcoD.camera(serial_port, receiver_address)
        self.buttonsDefinition()
        
    def initThermaCam(self):
        self.a40 = thermaCam.thermacam(self.serialThermaList.currentText())
        self.thermaBtnDefinition()
    
    def sendPreset(self):
        choice = str(self.PresetMenu.currentText())
        preset_number = int(self.PresetNumber.value())
        if choice == "Set Preset":
            self.camera1.setPreset(preset_number)
        elif choice == "Go To Preset":
            self.camera1.goToPreset(preset_number)
        elif choice == "Clear Preset":
            self.camera1.clearPreset(preset_number)
    
    def newOnkeyPressEvent(self,e):
        if e.isAutoRepeat():
            return
        else:
            if e.key() == QtCore.Qt.Key_I:
                self.camera1.up()
                #self.btnUp.SIGNAL("pressed")
            elif e.key() == QtCore.Qt.Key_K:
                self.camera1.down()
            elif e.key() == QtCore.Qt.Key_J:
                self.camera1.left()
            elif e.key() == QtCore.Qt.Key_L:
                self.camera1.right()
            elif e.key() == QtCore.Qt.Key_Space:
                self.camera1.stop()

    def newOnkeyReleaseEvent(self, e):
        if not e.isAutoRepeat():
            self.camera1.stop()
            
    def zoom(self):
        self.a40.zoom(float(self.zoomPower.value()))
        
    def rangeTemp(self):
        self.a40.setRange(float(self.lowTemp.value()), float(self.highTemp.value()))
    
    def rangeTempAuto(self):
        self.a40.autoAdj('on')
    
    def doImgAction(self):
        actionImg = str(self.getOrSave.currentText())
        imgName = str(self.imgName.text())
        if actionImg == "Save Image":
            self.a40.saveImage(imgName)
        elif actionImg == "Get Image":
            self.a40.getImage(imgName)
        elif actionImg == "Remove Image":
            cmdToSend = 'rm ' + imgName
            self.a40.writeCmd('cd \images')
            self.a40.writeCmd(cmdToSend)
        self.a40.uart.open()
        self.a40.uart.write(('\rls \\images\r').encode('utf-8'))
        listOfImages = []
        listOfFiles = self.a40.uart.readall().decode('utf-8')
        for a in listOfFiles.split():
            if a.endswith('.jpg'):
                listOfImages.append(a)
        
        print(listOfFiles)
        print(listOfImages)
        self.imgList.setPlainText(str(listOfImages))
        self.a40.uart.close()
            
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    MainWindow = camIRMain()
    MainWindow.show()
    sys.exit(app.exec_())
    
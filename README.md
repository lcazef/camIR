# CamIR

## Getting Started

This program has been created to remote a PTZ Tourelle and a FLIR thermal camera.

It can be used with Videotec DTRX3 receiver, or any receiver able to communicate with the Pelco D Protocol.
The thermal camera used during development is a FLIR ThermoVision A40M.


## Prerequisites

As both devices are remoted through serial port, you will need a computer with 2 serial (DB9) ports.


This program is written for Python 3.6. The best way to use it is by installing Anaconda, and creating a dedicated environment including the following libraries :

 - PyQt4, for the GUI
 - PySerial, for the communication through serial ports.

## How To Use

### Tourelle

 - Open a terminal
 - Activate the Anaconda environment previously created
 - Run camIR.py module with Python3
 - Select the correct serial port and click 'OK'.

### Camera

 - Open a terminal
 - Activate the Anaconda environment previously created
 - Run Python3
 - Import all the modules from thermaCam.py
 - Create a thermacam() object

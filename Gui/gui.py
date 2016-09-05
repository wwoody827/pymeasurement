#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
For testing rapid updates of ScatterPlotItem under various conditions.

(Scatter plots are still rather slow to draw; expect about 20fps)
"""

## Add path to library (just for examples; you do not need this)
import init
import math

from pyqtgraph.Qt import QtGui, QtCore, USE_PYSIDE, USE_PYQT5
import numpy as np
import pyqtgraph as pg
from pyqtgraph.ptime import time

from Driver.Keithley import Keithley_2400

app = QtGui.QApplication([])

# from ScatterPlotSpeedTestTemplate_pyqt import Ui_Form
from GuiK2400 import Ui_MainWindow
win = QtGui.QMainWindow()
win.setWindowTitle('Test pyMeasurement')
ui = Ui_MainWindow()
ui.setupUi(win)
win.show()

p = ui.graphicsView
p.setRange(xRange=[0, 1000], yRange=[-100, 100])

ptr = 0
fps = None

sinCurveX = [0]
sinCurveY = [0]

# Setting up measurement equipement
topGate = Keithley_2400(20)
backGate = Keithley_2400(21)
HallVoltage = SR830(4)

# Setting up measurement data file


def measurement():
    global sinCurveX, sinCurveY, ptr
    p.clear()
    ptr += 1
    sinCurveX.append(ptr)
    sinCurveY.append(math.sin(ptr/31.420))
    curve = pg.ScatterPlotItem(x=sinCurveX, y=sinCurveY, pen='w', brush='b', pxMode= True)
    p.addItem(curve)
    
    #p.repaint()
    #app.processEvents()  ## force complete redraw for every plot

def control():
    print(time())


# set updating frequency
MeasTimer = QtCore.QTimer()
MeasTimer.timeout.connect(update)
MeasTimer.start(1000)

CtrlTimer = QtCore.QTimer()


## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

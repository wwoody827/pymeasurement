## Add path to library (just for examples; you do not need this)
import init
import math

from pyqtgraph.Qt import QtGui, QtCore, USE_PYSIDE, USE_PYQT5
import numpy as np
import pyqtgraph as pg
from pyqtgraph.ptime import time

from Driver.Keithley.Keithley_2400 import Keithley_2400

app = QtGui.QApplication([])

from Keithley_2400Gui import Ui_Form
win = QtGui.QWidget()
win.setWindowTitle('Keithley_2400 Front Panel')
ui = Ui_Form()
ui.setupUi(win)
win.show()

# init Device
gpibAddress = 20
global K2400


setpoint = 0
nowWrite = 0
accerFastV = 0.1
accerSlowV = 0.01

accerFastI = 1e-6
accerSlowI = 1e-8


scanTime = 50 #ms
rate = accerSlowV

ui.gpibAddrInputBox.setText(str(gpibAddress))
ui.accerFast.setText(str(accerFastV))
ui.accerSlow.setText(str(accerSlowV))
ui.slowSelect.setChecked(True)

# set timer
MeasTimer = QtCore.QTimer()
ScanTimer = QtCore.QTimer()
filename = '20.dat'


def deviceInit():
  global gpibAddress, filename
  global K2400
  K2400 = Keithley_2400(gpibAddress)
  sourStats = K2400.getSourMode()
  gpibAddress = int(ui.gpibAddrInputBox.text())
  filename = "{:d}.dat".format(gpibAddress)
  if sourStats == 'VOLT':
    ui.sourVolt.setChecked(True)

  elif sourStats == 'CURR':
    ui.sourCurr.setChecked(True)
  else:
    ui.sourVolt.setChecked(False)
    ui.sourCurr.setChecked(False)
  

  if K2400.outpMode == 'ON':
    MeasTimer.start(100)
    ui.outputStatsDisp.setText("Output: ON")
  elif K2400.outpMode == 'OFF':
    ui.outputStatsDisp.setText("Output: OFF")
    MeasTimer.stop()
  print("Connected!")



def changeOutput():
  global K2400, MeasTimer
  if K2400.outpMode == 'OFF':
    K2400.setOutp('ON')
    MeasTimer.start(100)
    ui.outputStatsDisp.setText("Output: ON")
  elif K2400.outpMode == 'ON':
    K2400.setOutp('OFF')
    ui.outputStatsDisp.setText("Output: OFF")
    MeasTimer.stop()
  else:
    pass
  
  
def readVal():
  global K2400
  values = K2400.readVal()
  ui.voltDisp.setNum(values[0])
  ui.currDisp.setNum(values[1])
  datafile = open(filename, 'w')
  datafile.write("{:f},{:f}".format(values[0],values[1]))


def scanStart():
  global scanTime, K2400, ScanTimer, setValue, nowWrite
  setValueInput = ui.settingValue.text()
  setValue = float(setValueInput)
  nowWrite = K2400.readVal()[0]
  ScanTimer.start(scanTime)

def scanStop():
  global scanTime, K2400, ScanTimer, setValue

  setValue = K2400.readVal()[0]
  ui.settingValue.setText(str(setValue))
  ScanTimer.stop()

def setRate():
  global accerFastV, accerFastI, accerSlowV, accerSlowI, scanTime, rate
  
  if ui.fastSelect.isChecked():
    accerFastV = float(ui.accerFast.text())
    rate = accerFastV
  elif ui.slowSelect.isChecked():
    accerSlowV = float(ui.accerSlow.text())
    rate = accerSlowV
  else:
    pass



def scanner():
  '''
  return next value write to device
  '''
  global scanTime, setValue, rate, K2400, nowWrite
  currentValue = K2400.readVal()[0]
  step = scanTime/1000 * rate

  if math.fabs(setValue - nowWrite) < step:
    value = setValue
    K2400.setSourLevel(value)
    nowWrite = setValue
    ScanTimer.stop()
  else:
    value = nowWrite + np.sign(setValue - nowWrite) * step
    K2400.setSourLevel(value)
    nowWrite = value
  ui.nowWriteOutputBox.setText(str(nowWrite))



# link button

MeasTimer.timeout.connect(readVal)
ScanTimer.timeout.connect(scanner)

ui.connectButton.clicked.connect(deviceInit)
ui.outputSelect.clicked.connect(changeOutput)
ui.scannerStart.clicked.connect(scanStart)
ui.scannerCancel.clicked.connect(scanStop)
ui.slowSelect.toggled.connect(setRate)
ui.fastSelect.toggled.connect(setRate)

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
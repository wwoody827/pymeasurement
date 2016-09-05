# 20160903 This driver is based on the Keithley_2000 driver in 
# PyLab project. I removed some dependencies (like pyqt) and updated to 
# pyvisa 1.8

import visa
import types
import logging
import numpy


def bool_to_str(val):
    '''
    Function to convert boolean to 'ON' or 'OFF'
    '''
    if val == True:
        return "ON"
    else:
        return "OFF"

class Keithley_2400:
    '''
    This is the driver for the Keithley 2400 source meter


    '''

    def __init__(self, address, reset=False,
            change_display=True, change_autozero=True):
        '''
        Initializes the Keithley_2400, and communicates with the wrapper.

        Input:
            name (string)           : name of the instrument
            address (string)        : GPIB address
            reset (bool)            : resets to default values
            change_display (bool)   : If True (default), automatically turn off
                                        display during measurements.
            change_autozero (bool)  : If True (default), automatically turn off
                                        autozero during measurements.
        Output:
            None
        '''
        # Initialize wrapper functions
        logging.info('Initializing instrument Keithley_2400')

        # Add some global constants
        self._address = address

        rm = visa.ResourceManager()
        self._visainstrument = rm.open_resource("GPIB::{:d}".format(self._address))


        self.sourMode = 'VOLT'
        self.sensMode = 'CURR'
        self.outpMode = 'OFF'
        # Add parameters to wrapper
    

        # Connect to measurement flow to detect start and stop of measurement
        # qt.flow.connect('measurement-start', self._measurement_start_cb)
        # qt.flow.connect('measurement-end', self._measurement_end_cb)

        if reset:
            self.reset()
        else:
            self.getAll()
            # self.get_all()
            # self.set_defaults()
            pass

# --------------------------------------
#           functions
# --------------------------------------

    def reset(self):
        '''
        Resets instrument to default values

        Input:
            None

        Output:
            None
        '''
        logging.debug('Resetting instrument')
        self._visainstrument.write("*RST")
        
        # self.get_all()

    def getAll(self):
        self.sourMode = self.getSourMode()
        self.outpMode = self.getOutpMode()

    def getSourMode(self):
        return self._visainstrument.query("SOUR:FUNC?")[0:4]

    def getOutpMode(self):
        status =  int(self._visainstrument.query(":OUTP:STAT?"))
        if status == 1:
            return 'ON'
        else:
            return 'OFF'

    def getSensMode(self):
        return self._visainstrument.query("SENS:FUNC?")

    def setSourMode(self, mode = 'VOLT'):
        if mode == 'VOLT':
            self.sourMode = 'VOLT'
        elif mode == 'CURR':
            self.sourMode = 'CURR'
        else:
            print("Error")
            self.sourMode = 'VOLT'
        self._visainstrument.write(":SOUR:FUNC {0}".format(self.sourMode))

    def setSourLevel(self, value):
        self._visainstrument.write(":SOUR:{}:LEV {:f}".format(self.sourMode, value))

    def setSensMode(self, sensMode):
        if sensMode == "VOLT":
            self.sensMode = 'VOLT'
        elif sensMode == 'CURR':
            self.sensMode = 'CURR'
        elif sensMode == 'RES':
            self.sensMode = 'RES'
        else:
            print("Error")
        self._visainstrument.write(":SENS:FUNC \"{}\"".format(self.sensMode))

    def setOutp(self, output):
        if output == 'ON':
            self.outpMode = 'ON'
        elif output == 'OFF':
            self.outpMode = 'OFF'
        else:
            print("Error")
            self.outpMode = 'ON'
        self._visainstrument.write(":OUTP {}".format(self.outpMode))

    def readVal(self):
        '''
        Resets instrument to default values

        Input:
            None

        Output:
            list of values
        '''
        readStr = self._visainstrument.query(":READ?")
        reading = readStr.split(',')
        return  [float(i) for i in reading]
    def close(self):
        self._visainstrument.close()

if __name__ == "__main__":
    testK2400 = Keithley_2400(20)
    print('init finished')
    print('start reseting')

    testK2400.setSourMode('VOLT')

    #testK2400.setSourLevel(1)
    #testK2400.setOutp('ON')
    #print(testK2400.readVal())
    #testK2400.setOutp('ON')
    print(testK2400.getSourMode())
    testK2400.close()


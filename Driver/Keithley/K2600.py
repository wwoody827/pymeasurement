from visa import instrument

class K2600():
    """ Keithley 2600 instrument class. """
    def __init__( self, address=26 ):
        self.ctrl = instrument( "GPIB::%s" % address )


    def close(self):
        """ closes the VISA instance (I think) """
        self.ctrl.close()


    def measure_current( self, channel='A' ):
        """ queries instrument, returns value """
        if channel=='A':
            return self.ctrl.ask( "print(smua.measure.i())" )
        elif channel=='B':
            return self.ctrl.ask( "print(smub.measure.i())" )
        else:
            raise ValueError("Invalid channel sent to function measure_current")


    def measure_voltage( self, channel='A' ):
        """ queries instrument, returns value """
        if channel=='A':
            return self.ctrl.ask( "print(smua.measure.v())" )
        elif channel=='B':
            return self.ctrl.ask( "print(smub.measure.v())" )
        else:
            raise ValueError("Invalid channel sent to function measure_voltage")


    def reset(self):
        """ resets instrument """
        self.ctrl.write( "reset()" )


    def reset_channel( self, channel='A' ):
        """ resets VISA channel """
        if channel=='A':
            self.ctrl.write( "smua.reset()" )
        elif channel=='B':
            self.ctrl.write( "smub.reset()" )
        else:
            raise ValueError("Invalid channel sent to function reset_channel")


    def set_measure_current_range( self, meas_range=None, channel='A' ):
        """ if *meas_range* is not specified, measurement will be set to autorange """
        if channel=='A':
            if src_range is None:
                self.ctrl.write(  "smua.measure.autorangei = smua.AUTORANGE_ON" )
            else:                         
                self.ctrl.write(  "smua.measure.rangei = %s" % meas_range )
        elif channel=='B':
            if src_range is None:
                self.ctrl.write(  "smub.measure.autorangei = smua.AUTORANGE_ON" )
            else:                         
                self.ctrl.write(  "smub.measure.rangei = %s" % meas_range )
        else:
            raise ValueError("Invalid channel sent to function set_measure_current_range")


    def set_current_compliance( self, compliance, channel='A' ):
        """ Set max output current level """
        if channel=='A':
            self.ctrl.write( "smua.source.limiti = %s" % compliance )
        elif channel=='B':
            self.ctrl.write( "smub.source.limiti = %s" % compliance )
        else:
            raise ValueError("Invalid channel sent to function set_current_compliance")

        
    def set_output_on( self, channel='A' ):
        """ turn on output """
        if channel=='A':
            self.ctrl.write( "smua.source.output = smua.OUTPUT_ON" )
        elif channel=='B':
            self.ctrl.write( "smub.source.output = smub.OUTPUT_ON" )
        else:
            raise ValueError("Invalid channel sent to function set_output_on")

        
    def set_output_off( self, channel='A' ):
        """ turn off output """
        if channel=='A':
            self.ctrl.write( "smua.source.output = smua.OUTPUT_OFF" )
        elif channel=='B':
            self.ctrl.write( "smub.source.output = smub.OUTPUT_OFF" )
        else:
            raise ValueError("Invalid channel sent to function set_output_off")

        
    def set_output_amps( self, amps, channel='A' ):
        """ set the output current in amps """
        if channel=='A':
            self.ctrl.write( "smua.source.leveli = %s" % amps )
        elif channel=='B':
            self.ctrl.write( "smub.source.leveli = %s" % amps )
        else:
            raise ValueError("Invalid channel sent to function set_output_amps")

        
    def set_output_volts( self, volts, channel='A' ):
        """ set the output voltage level in volts """
        if channel=='A':
            self.ctrl.write( "smua.source.levelv = %s" % volts )
        elif channel=='B':
            self.ctrl.write( "smub.source.levelv = %s" % volts )
        else:
            raise ValueError("Invalid channel sent to function set_output_volts")

        
    def set_source_type_current( self, src_range=None, channel='A' ):
        """
        set the smu channel to source current (in amps)
        if `src_range` is not specified, smu source will be set to autorange
        """
        if channel=='A':
            self.ctrl.write( "smua.source.func = smua.OUTPUT_DCAMPS" )
            if src_range is None:
                self.ctrl.write(  "smua.source.autorangei = smua.AUTORANGE_ON" )
            else:                         
                self.ctrl.write(  "smua.source.rangev = %s" % src_range )
        elif channel=='B':
            self.ctrl.write( "smub.source.func = smub.OUTPUT_DCAMPS" )
            if src_range is None:
                self.ctrl.write(  "smub.source.autorangei = smub.AUTORANGE_ON" )
            else:                         
                self.ctrl.write(  "smub.source.rangev = %s" % src_range )
        else:
            raise ValueError("Invalid channel sent to function set_source_type_current")


    def set_source_type_voltage( self, src_range=None, channel='A' ):
        """
        set the smu channel to source volts
        if `src_range` is not specified, smu source will be set to autorange
        """
        if channel=='A':
            self.ctrl.write( "smua.source.func = smua.OUTPUT_DCVOLTS" )
            if src_range is None:
                self.ctrl.write(  "smua.source.autorangev = smua.AUTORANGE_ON" )
            else:                         
                self.ctrl.write(  "smua.source.rangev = %s" % src_range )
        elif channel=='B':
            self.ctrl.write( "smub.source.func = smub.OUTPUT_DCVOLTS" )
            if src_range is None:
                self.ctrl.write(  "smub.source.autorangev = smub.AUTORANGE_ON" )
            else:                         
                self.ctrl.write(  "smub.source.rangev = %s" % src_range )
        else:
            raise ValueError("Invalid channel sent to function set_source_type_voltage")


    def write( self, command_string ):
        """ send the supplied string to the instrument """
        self.ctrl.write( command_string )
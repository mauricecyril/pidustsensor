#!/usr/bin/env python

# PPD42NS.py
# 2015-11-22
# Public Domain
# Original Script from http://abyz.co.uk/rpi/pigpio/examples.html
# Adaptions from https://github.com/andy-pi/weather-monitor/blob/master/air_quality.py

# On the Raspbery Pi make sure to install pigpio using Apt
# $ sudo apt-get install pigpio python-pigpio python3-pigpio
#
# Once installed make sure to run the pidpio daemon before
# running this script
#
# $ sudo pigpiod
# $ python pidustsensor.py
# or
# $ python3 pidustsensor.py

from __future__ import print_function
import math
import pigpio
# also import writer for writing CSV logs
from csv import writer

class sensor:
    """
    A class to read a Shinyei PPD42NS Dust Sensor, e.g. as used
    in the Grove dust sensor.
    
    This code calculates the percentage of low pulse time and
    calibrated concentration in particles per 1/100th of a cubic
    foot at user chosen intervals.
    
    You need to use a voltage divider to cut the sensor output
    voltage to a Pi safe 3.3V (alternatively use an in-line
    20k resistor to limit the current at your own risk).
    """

    def __init__(self, pi, gpio):
        """
        Instantiate with the Pi and gpio to which the sensor
        is connected.
        """
        
        self.pi = pi
        self.gpio = gpio
        
        self._start_tick = None
        self._last_tick = None
        self._low_ticks = 0
        self._high_ticks = 0

        pi.set_mode(gpio, pigpio.INPUT)

        self._cb = pi.callback(gpio, pigpio.EITHER_EDGE, self._cbf)

    def read(self):
        """
        Calculates the percentage low pulse time and calibrated
        concentration in particles per 1/100th of a cubic foot
        since the last read.

        For proper calibration readings should be made over
        30 second intervals.
        
        Returns a tuple of gpio, percentage, and concentration.
        """
        interval = self._low_ticks + self._high_ticks

        if interval > 0:
            ratio = float(self._low_ticks)/float(interval)*100.0
            conc = 1.1*pow(ratio,3)-3.8*pow(ratio,2)+520*ratio+0.62;
        else:
            ratio = 0
            conc = 0.0

        self._start_tick = None
        self._last_tick = None
        self._low_ticks = 0
        self._high_ticks = 0

        return (self.gpio, ratio, conc)

    def _cbf(self, gpio, level, tick):

        if self._start_tick is not None:

            ticks = pigpio.tickDiff(self._last_tick, tick)

            self._last_tick = tick

            if level == 0: # Falling edge.
                self._high_ticks = self._high_ticks + ticks

            elif level == 1: # Rising edge.
                self._low_ticks = self._low_ticks + ticks

            else: # timeout level, not used
                pass

        else:
            self._start_tick = tick
            self._last_tick = tick
         


if __name__ == "__main__":

    from datetime import datetime
    import time
    import pigpio
    import PPD42NS

    pi = pigpio.pi() # Connect to a remote pi or 'localhost'

    # Select the pi GPIO pin that is connected to the sensor
    # Make sure to use the Broadcom GPIO Pin number
    s = PPD42NS.sensor(pi, 8) 
   
    # Option to prompt for filename:
    ##logfilename = input("Please enter a name for the logfile.") 
    ##with open(logfilename + '.csv', 'w', newline='') as f:

    # Create a specific and static csv log file
    with open('airqualitylog.csv', 'w', newline='') as f:
    # Remove the above line if you want to use the prompt for logfile name function
		
        data_writer = writer(f)
        #write header for csv log file
        data_writer.writerow(['GPIO','Date Time Stamp', 'Ratio', 'Concentration (PCS  per 0.01 cubic foot)', 'Concentration (PCS per cubic metre)', 'US AQI (Should be average of a 24h reading)'])
        
        while True:
        
            time.sleep(30) # Use 30 for a properly calibrated reading.
            
            # Read the values from the sensor
            # get the gpio, ratio and concentration in particles / 0.01 ft3
            g, r, c = s.read()
            
            if (c == 1114000.62):
                print("Error\n")
                continue
	  
	        if c < 0:
                raise ValueError('Concentration cannot be a negative number')

            # Convert concentration of PM2.5 particles per 0.01 cubic feet to µg/ metre cubed
            # this method outlined by Drexel University students (2009) and is an approximation
            # does not contain correction factors for humidity and rain
      
	        # Assume all particles are spherical, with a density of 1.65E12 µg/m3
            densitypm25 = 1.65 * math.pow(10, 12)
        
            # Assume the radius of a particle in the PM2.5 channel is .44 µm
            rpm25 = 0.44 * math.pow(10, -6)
        
            # Volume of a sphere = 4/3 * pi * radius^3
            volpm25 = (4/3) * math.pi * (rpm25**3)
        
            # mass = density * volume
            masspm25 = densitypm25 * volpm25
        
            # parts/m3 =  parts/foot3 * 3531.5
            # µg/m3 = parts/m3 * mass in µg
            concentration_ugm3 = c * 3531.5 * masspm25
      
            # Convert concentration of PM2.5 particles in µg/ metre cubed to the USA 
            # Environment Agency Air Quality Index - AQI
            # https://en.wikipedia.org/wiki/Air_quality_index
            # Computing_the_AQI
            # https://github.com/intel-iot-devkit/upm/pull/409/commits/ad31559281bb5522511b26309a1ee73cd1fe208a?diff=split
            # input should be 24 hour average of ugm3, not instantaneous reading
      
        
            cbreakpointspm25 = [ [0.0, 12, 0, 50],\
                            [12.1, 35.4, 51, 100],\
                            [35.5, 55.4, 101, 150],\
                            [55.5, 150.4, 151, 200],\
                            [150.5, 250.4, 201, 300],\
                            [250.5, 350.4, 301, 400],\
                            [350.5, 500.4, 401, 500], ]
                        
            C = concentration_ugm3
        
            if C > 500.4:
                aqi = 500

            else:
                for breakpoint in cbreakpointspm25:
                    if breakpoint[0] <= C <= breakpoint[1]:
                        Clow = breakpoint[0]
                        Chigh = breakpoint[1]
                        Ilow = breakpoint[2]
                        Ihigh = breakpoint[3]
                        aqi = (((Ihigh-Ilow)/(Chigh-Clow))*(C-Clow))+Ilow
      
         
            # Store values in a variable
            aqdata = g, timestamp, r, int(c), concentration_ugm3, aqi
         
            # Store values in CSV log file
            data_writer.writerow(aqdata) 
         
            # Print values to console
            print("gpio={} timestamp={} ratio={:.1f} conc={} particles per 0.01 cubic foot concSI={} particles per cubic metre aqi={}".
                format(g, timestamp, r, int(c)), concentration_ugm3, aqi)
         
            # Print
            
        pi.stop() # Disconnect from Pi.


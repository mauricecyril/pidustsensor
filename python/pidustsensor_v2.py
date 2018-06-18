#!/usr/bin/env python

# PPD42NS.py
# 2015-11-22
# Public Domain
# Original Script from http://abyz.co.uk/rpi/pigpio/examples.html
# Adaptions from https://github.com/andy-pi/weather-monitor/blob/master/air_quality.py


####### Instructions ########################
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

####### Wiring Options ######################
# +-----------------------------------------+
#  |                                         |
#  |  Shinyei PPD42NS  / Grove Dust Sensor   |
#  |  (Sensor components facing you          |           
#  |                                         |
#  |    |+|        |+|                       |          
#  |    SL2 POT    CN1 POT                   |
#  +-----------------------------------------+
#  |    Pin Number                           |
#  |                                         |          
#  |     |     |     |     |     |           |
#  |     5     4     3     2     1           |       
#  |     |     |     |     |     |           |
#  +-----------------------------------------+
#        |     |     |     |     | 
#        |     |     |     |  GND (Black)
#        |     |     |     |     | 
#        |     |  5V (Red) |     | 
#        |     |     |     |     | 
#        |   PM2.5   |     |     |
#        |     |     |     |     | 
#        |     |     |   PM1.0   |
#        |     |     |     |     |
#   Threshold  |     |     |     |
#   for Pin 2  |     |     |     | 
#        |     |     |     |     | 
#        |     |     |     |     | 
#
# CN : S5B-EH(JST)
# 1 : COMMON(GND) [Black Wire on Grove Sensor]
# 2 : OUTPUT(P2) [Not used on Grove Connectr] [Can be used for PM1.0]
# 3 : INPUT(5VDC 90mA) [Red Wire on Grove Sensor]
# 4 : OUTPUT(P1) [Yellow Wire on Grove Sensor] [Used for PM2.5 mesurements]
# 5 : INPUT(T1)･･･FOR THRESHOLD FOR [P2] [Not used on Grove Connector]
#############################################



# Using a Bi-Directional Logic Level Converter
#  +-----------------------------------------+
#  |                                         |
#  |  Shinyei PPD42  / Grove Dust Sensor     |
#  |  (Sensor facing you)                    |           
#  |                                         |
# |    |+|        |+|                       |          
#  |    SL2 POT    CN1 POT                   |
#  +-----------------------------------------+
#  |    Pin Number                           |
#  |                                         |          
#  |     |     |     |     |     |           |
#  |     5     4     3     2     1           |       
#  |     |     |     |     |     |           |
#  +-----------------------------------------+
#        |     |     |     |     | 
#        |     |     |     |  GND (Black)
#        |     |     |     |     | 
#        |     |  5V (Red) |     | 
#        |     |     |     |     | 
#        |   PM2.5   |     |     |
#        |     |     |     |     |                 +-----------------------+
#        |     |     |   PM1.0   |                 |Bi-Direction Logic     |
#        |     |     |     |     |                 |Level Converter        |
#        |     |     |     |     |                 +-----------------------+
#   Threshold  |     |     |     +--(1) GND--------|  GND              GND |----[[RPi GND Pin]]
#   for Pin 2  |     |     |                       |                       |
#        |     |     |     +-----(2) PM1.0---------|  B1               A1  |----[[RPi GPIO Pin]]
#        |     |     |                             |                       |
#        |     |     +-----------(3) 5V------+-----|  HV               LV  |----[[RPi 3.3V Pin]]
#        |     |                             |     |                       |
#        |     |                             |     |                       |
#        |     |             [[RPi 5V Pin]]--+     |                       |
#        |     |                                   |                       |
#        |     +-----------------(4) PM2.5---------|  B2               A2  |----[[RPi GPIO Pin]]
#        |                                         +-----------------------+
#        |
#   [[Not used]]
#
#
#############################################


# Using a Voltage Divider (At your own risk)
#
#  +-----------------------------------------+
#  |                                         |
#  |  Shinyei PPD42  / Grove Dust Sensor     |
#  |  (Sensor facing you)                    |           
#  |                                         |
#  |    |+|        |+|                       |          
#  |    SL2 POT    CN1 POT                   |
#  +-----------------------------------------+
#  |    Pin Number                           |
#  |                                         |          
#  |     |     |     |     |     |           |
#  |     5     4     3     2     1           |       
#  |     |     |     |     |     |           |
#  +-----------------------------------------+
#        |     |     |     |     | 
#        |     |     |     |  GND (Black)
#        |     |     |     |     | 
#        |     |  5V (Red) |     | 
#        |     |     |     |     | 
#        |   PM2.5   |     |     |
#        |     |     |     |     | 
#        |     |     |   PM1.0   |
#        |     |     |     |     |     1 kΩ        1 kΩ resistor
#   Threshold  |     |     |     +----[_____]-----[_____]------+--------> [[Pi GND Pin]]
#   for Pin 2  |     |     |                                   |
#        |     |     |     |                  1 kΩ resistor    |
#        |     |     |     +----------------[_____]------------+--------> [[Pi GPIO Pin 7]]
#        |     |     |                                         |
#        |     |     +-----------------> [[Pi 5V Pin]]         |
#        |     |                                               |
#        |     |                              1 kΩ resistor    |
#        |     +----------------------------[_____]------------+--------> [[Pi GPIO Pin 8]]
#        |
#        |
#   [[Not used]]
#
#
#############################################

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

    # Method for calculating Ratio and Concentration
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

    pi = pigpio.pi('localhost') # Connect to a remote pi or 'localhost'

    # Select the pi GPIO pin that is connected to the sensor
    # For PM2.5 Readings, connected to Pin 4 of the Sensor
    # Make sure to use the Broadcom GPIO Pin number
    s25 = PPD42NS.sensor(pi, 8)

    # Select the pi GPIO pin that is connected to the sensor
    # For PM10 Readings, connected to Pin 2 of the Sensor
    # Make sure to use the Broadcom GPIO Pin number
    s10 = PPD42NS.sensor(pi, 7)
    
   
    # Option to prompt for filename:
    ##logfilename = input("Please enter a name for the logfile.") 
    ##with open(logfilename + '.csv', 'w', newline='') as f:

    # Create a specific and static csv log file
    with open('airqualitylog.csv', 'w', newline='') as f:
    # Remove the above line if you want to use the prompt for logfile name function
		
        data_writer = writer(f)
        #write header for csv log file
        data_writer.writerow(['Date Time Stamp', 'Ratio for PM2.5', 'PM2.5 Concentration (PCS  per 0.01 cubic foot)', 'Concentration Count for 2.5 PM', 'PM2.5 Concentration (PCS per cubic metre)', 'US AQI for PM2.5 (Should be average of a 24h reading)', 'Ratio for PM10', 'PM10 Concentration (PCS  per 0.01 cubic foot)', 'Concentration Count for 10 PM', 'PM10 Concentration (PCS per cubic metre)', 'US AQI for PM10 (Should be average of a 24h reading)'])
        
        while True:
        
            time.sleep(30) # Use 30 for a properly calibrated reading.

            # Get the current time of the reading
            timestamp = datetime.now()
            
            # Read the PM2.5 values from the sensor
            # get the gpio, ratio and concentration in particles / 0.01 ft3
            g25, r25, c25 = s25.read()

            # do some checks on the concentration reading and print errors
            if (c25 == 1114000.62):
                print("Error\n")
                continue
	  
            if c25 < 0:
                raise ValueError('Concentration cannot be a negative number')


            # Read the PM10 values from the sensor
            # get the gpio, ratio and concentration in particles / 0.01 ft3
            g10, r10, c10 = s10.read()
            
            # do some checks on the concentration reading and print errors
            if (c10 == 1114000.62):
                print("Error\n")
                continue
	  
            if c10 < 0:
                raise ValueError('Concentration cannot be a negative number')


            # Special Calculations for differentiating between two particulate sizes
            # Note: Not sure why P10 calculation is subtracted from PM2.5
            # Maybe hreshold input (IN1) is left unsed, but it will be used later as a way to
            # split particule by size, and hence detect both PM10 and PM2.5 particules.
            PM10count = c10
            PM25count = c25 - c10 # Not sure why this is required


            # Convert conentrations to µg/ metre cubed
            # Convert concentration of PM2.5 and PM10 particles per 0.01 cubic feet to µg/ metre cubed
            # this method outlined by Drexel University students (2009) and is an approximation
            # does not contain correction factors for humidity and rain
      
            # Assume all particles are spherical, with a density of 1.65E12 µg/m3
            density = 1.65 * math.pow(10, 12)
        
            # PM2.5 Values
            # Assume the radius of a particle in the PM2.5 channel is .44 µm
            rpm25 = 0.44 * math.pow(10, -6)
        
            # Volume of a PM2.5 sphere = 4/3 * pi * radius^3
            volpm25 = (4/3) * math.pi * (rpm25**3)
        
            # mass = density * volume
            masspm25 = density * volpm25
        
            # parts/m3 =  parts/foot3 * 3531.5
            # µg/m3 = parts/m3 * mass in µg
            concentration_ugm3_pm25 = PM25count * 3531.5 * masspm25 # or use c25 instead of PM25count


            # PM10 Values
            # Assume the radius of a particle in the PM10 channel is 2.6 µm
            rpm10 = 2.6 * math.pow(10, -6)
        
            # Volume of a PM10 sphere = 4/3 * pi * radius^3
            volpm10 = (4/3) * math.pi * (rpm10**3)
        
            # mass = density * volume
            masspm10 = density * volpm10
        
            # parts/m3 =  parts/foot3 * 3531.5
            # µg/m3 = parts/m3 * mass in µg
            concentration_ugm3_pm10 = PM10count * 3531.5 * masspm10 # Or use c10 instead of PM10count



      
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
                        
            C = concentration_ugm3_pm25
        
            if C > 500.4:
                aqi25 = 500

            else:
                for breakpoint in cbreakpointspm25:
                    if breakpoint[0] <= C <= breakpoint[1]:
                        Clow = breakpoint[0]
                        Chigh = breakpoint[1]
                        Ilow = breakpoint[2]
                        Ihigh = breakpoint[3]
                        aqi25 = (((Ihigh-Ilow)/(Chigh-Clow))*(C-Clow))+Ilow


      
            # Convert concentration of PM10 particles in µg/ metre cubed to the USA 
            # Environment Agency Air Quality Index - AQI
            # https://en.wikipedia.org/wiki/Air_quality_index
            # Computing_the_AQI
            # https://github.com/intel-iot-devkit/upm/pull/409/commits/ad31559281bb5522511b26309a1ee73cd1fe208a?diff=split
            # input should be 24 hour average of ugm3, not instantaneous reading
      
        
            cbreakpointspm10 = [ [0, 54, 0, 50],\
                            [55, 154, 51, 100],\
                            [155, 254, 101, 150],\
                            [255, 354, 151, 200],\
                            [355, 424, 201, 300],\
                            [425, 504, 301, 400],\
                            [505, 604, 401, 500], ]
                        
            D = concentration_ugm3_pm10
        
            if D > 604:
                aqi10 = 500

            else:
                for breakpoint in cbreakpointspm10:
                    if breakpoint[0] <= D <= breakpoint[1]:
                        Clow = breakpoint[0]
                        Chigh = breakpoint[1]
                        Ilow = breakpoint[2]
                        Ihigh = breakpoint[3]
                        aqi10 = (((Ihigh-Ilow)/(Chigh-Clow))*(C-Clow))+Ilow
      

         
            # Store values in a variable
            aqdata = timestamp, r25, int(c25), int(PM25count), int(concentration_ugm3_pm25), int(aqi25), r10, int(c10), int(PM10count), int(concentration_ugm3_pm10), int(aqi10)
         
            # Store values in CSV log file
            data_writer.writerow(aqdata) 
         
            # Print values to console
            print("timestamp={} ratio={:.1f} for PM10 conc={} PM2.5 particles per 0.01 cubic foot concCount={} PM2.5 Count concSI={} PM2.5 particles per cubic metre aqi={} ratio={:.1f} for PM10 conc={} PM10 particles per 0.01 cubic foot concCount={} PM10 Count concSI={} PM10 particles per cubic metre aqi={}" .
                format(timestamp, r25, int(c25), int(PM25count), int(concentration_ugm3_pm25), int(aqi25), r10, int(c10), int(PM10count), int(concentration_ugm3_pm10), int(aqi10)))
         
            # Print
            
        pi.stop() # Disconnect from Pi.


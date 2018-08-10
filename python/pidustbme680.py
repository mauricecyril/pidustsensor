#!/usr/bin/env python

# pidustbme680.py
# GNU General Public License v3.0

# Script to log Shinyei PPD42  / Grove Dust Sensor and Pimoroni / BOSCH BME680 breakout
# Readings are stored on a CSV file and SQLite3 DB
# Derived from PPD42NS.py (2015-11-22 Public Domain) Original Script located at http://abyz.co.uk/rpi/pigpio/examples.html
# Adaptions from https://github.com/andy-pi/weather-monitor/blob/master/air_quality.py
# Added https://shop.pimoroni.com/products/bme680-breakout scripts from https://github.com/pimoroni/bme680/blob/master/examples/read-all.py


#############################################

from __future__ import print_function
import math
import pigpio
import bme680
import time
from Adafruit_IO import Client, RequestError, Feed
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
    from Adafruit_IO import Client, RequestError, Feed
    import time
    import bme680
    import pigpio
    import pidustbme680 # import this script
    import sqlite3
    import sys
    
      
    # Setup BME680 Sensor
    sensor = bme680.BME680()
    
    #print("Calibration data:")
    #for name in dir(sensor.calibration_data):

    #    if not name.startswith('_'):
    #        value = getattr(sensor.calibration_data, name)

    #    if isinstance(value, int):
    #        print("{}: {}".format(name, value))

    # These oversampling settings can be tweaked to 
    # change the balance between accuracy and noise in
    # the data.

    sensor.set_humidity_oversample(bme680.OS_2X)
    sensor.set_pressure_oversample(bme680.OS_4X)
    sensor.set_temperature_oversample(bme680.OS_8X)
    sensor.set_filter(bme680.FILTER_SIZE_3)
    sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
    
    print("\n\nInitial reading:")
    for name in dir(sensor.data):
        value = getattr(sensor.data, name)

        if not name.startswith('_'):
            print("{}: {}".format(name, value))

    sensor.set_gas_heater_temperature(320)
    sensor.set_gas_heater_duration(150)
    sensor.select_gas_heater_profile(0)

    # Up to 10 heater profiles can be configured, each
    # with their own temperature and duration.
    # sensor.set_gas_heater_profile(200, 150, nb_profile=1)
    # sensor.select_gas_heater_profile(1)
    
    # Setup PiGPIO
    pi = pigpio.pi('localhost') # Connect to a remote pi or 'localhost'

    # Select the pi GPIO pin that is connected to the sensor
    # For PM2.5 Readings, connected to Pin 4 of the Sensor
    # Make sure to use the Broadcom GPIO Pin number
    s25 = pidustbme680.sensor(pi, 18)

    # Select the pi GPIO pin that is connected to the sensor
    # For PM1.0 Readings, connected to Pin 2 of the Sensor
    # Make sure to use the Broadcom GPIO Pin number
    s10 = pidustbme680.sensor(pi, 17)
    
    # Setup Adafruit IO
    # Set to your Adafruit IO key.
    # Remember, your key is a secret,
    # so make sure not to publish it when you publish this code!
    ADAFRUIT_IO_KEY = 'YOUR_AIO_KEY'

    # Set to your Adafruit IO username.
    # (go to https://accounts.adafruit.com to find your username)
    ADAFRUIT_IO_USERNAME = 'YOUR_AIO_USERNAME'

    # Create an instance of the REST client.
    aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

    # Assign a feed for each environment sensor reading
    # Make sure that these feeds have been setup already
    # 
    # Example: io_c25 = aio.feeds('environment-sensor.c25')
    # In above example the "group" is "environment-sensor"
    # And the "feed" name is "c25"

    io_c25 = aio.feeds('environment-sensor.c25')
    io_c10 = aio.feeds('environment-sensor.c10')
    io_temp = aio.feeds('environment-sensor.temp')
    io_pres = aio.feeds('environment-sensor.pres')
    io_hum = aio.feeds('environment-sensor.hum')
    io_gas = aio.feeds('environment-sensor.gas')
    
    
    # Option to prompt for filename:
    ##logfilename = input("Please enter a name for the logfile.") 
    ##with open(logfilename + '.csv', 'w', newline='') as f:

    # Create a specific and static csv log file
    with open('/media/pi/envirosensorlog.csv', 'w', newline='') as f:
    # Remove the above line if you want to use the prompt for logfile name function
		
        data_writer = writer(f)
        #write header for csv log file
        data_writer.writerow(['Date Time Stamp',
                              'Ratio for PM2.5 (P2 or Pin4) (r25)',
                              'Raw Readings of PM2.5 Concentration (PCS per 0.01 cubic foot) (c25)',
                              'Ratio for PM1.0 (P1 or Pin2) (r10)',
                              'Raw readings of PM1.0 Concentration (PCS  per 0.01 cubic foot) (c10)',
                              'Temperature (Celsius)',
                              'Pressure (hPa)',
                              'Humidity (%RH)',
                              'Gas Resistance (Ohms)'])

        while True:
        
            time.sleep(30) # Use 30 for a properly calibrated reading.

            # Get the current time of the reading
            timestamp = datetime.now()
                       
            if sensor.get_sensor_data():
                temp = sensor.data.temperature
                pres = sensor.data.pressure
                hum = sensor.data.humidity
  
                if sensor.data.heat_stable:
                    gas = sensor.data.gas_resistance
  
                else:
                    gas = 0

            
            # Read the PM2.5 values from the sensor. Particles Greater than 2.5 micrometers.
            # get the gpio, ratio and concentration in particles / 0.01 ft3
            g25, r25, c25 = s25.read()

            # Read the PM1.0 values from the sensor. Particles Greater than 1 micrometers.
            # get the gpio, ratio and concentration in particles / 0.01 ft3
            g10, r10, c10 = s10.read()

            # Fix Errors if the Shinyei PPD42NS  / Grove Dust Sensor Returns an error
            if r25 == 100.00:
                r25 = 0
                
            if c25 == 1114000.62:
                c25 = 0
                
            if r10 == 100.00:
                r10 = 0
                
            if c10 == 1114000.62:
                c10 = 0
            
            # Store values in a variable
            aqdata = timestamp, r25, int(c25), r10, int(c10), temp, pres, hum, gas
         
            # SQLite3 Data Storage
            # Create a variable used to connect to the Database
            con = sqlite3.connect('envirosensorlog.db')   #Change envirosensorlog.db to your database name
            
            # Insert the variables used in aqdata into the database
            with con:
                curs = con.cursor() 
                curs.execute("INSERT INTO envirosensorlog(datetimestamp, r25_db, c25_db, r10_db, c10_db, temp_db, pres_db, hum_db, gas_db) VALUES(?,?,?,?,?,?,?,?,?)",(timestamp, r25, c25, r10, c10, temp, pres, hum, gas))  
            
            # commit the changes
            con.commit()
            con.close()
            
            # Store values in CSV log file
            data_writer.writerow(aqdata)
            
            # Send values to ADAFRUIT.IO
            aio.send_data(io_c25.key, c25)
            aio.send_data(io_c10.key, c10)
            aio.send_data(io_temp.key, temp)
            aio.send_data(io_pres.key, pres)
            aio.send_data(io_hum.key, hum)
            aio.send_data(io_gas.key, gas)
            
            # Print values to console
            print("Timestamp of Readings = {} \n PM2.5 (P2 or Pin4):  Ratio = {:.1f}, PM > 2.5 µg PCS Conc = {} µg/ft3  \n PM1.0 (P1 or Pin2):   Ratio = {:.1f}, PM > 1.0 µg PCS Conc = {} µg/ft3 \n BME 680 Readings:   Temp = {:.2f} C, Pressure = {:.2f} hPa, Humidity = {:.2f} %RH, Gas Resistance = {} Ohms  \n " .
                format(timestamp, r25, int(c25), r10, int(c10), temp, pres, hum, gas))
           
            # Print
            
        pi.stop() # Disconnect from Pi.


# Reference Information on Sensor
# http://www.shinyei.co.jp/stc/eng/optical/main_ppd42.html
# Detectable Particle Size: Over 1.0µm, Sensor uses the counting method not weight\
# Units are measured in pcs/L or pcs/0.01cf
#
# http://lantaukwcounter.blogspot.com/2015/10/pdd42-sensor-can-it-measure-pm10-and.html
# P1 for particles > 1 micron, P2 for particles > 2.5 micron
# Based on this it might be possible to capture AQI for PM2.5 but not AQI for PM10
# The script references PM10 but it appears the actual measure is particles greater than 1 micron
#
# https://www.engineeringtoolbox.com/particle-sizes-d_934.html
# one micron is one-millionth of a metre
# 1 micron = 10-6 m
# 1 micron = 1000 nano metre

# Airborne particles
# Airborne particles are solids suspended in the air.

# Larger particles - larger then 100 μm
# terminal velocities > 0.5 m/s
# fall out quickly
# includes hail, snow, insect debris, room dust, soot aggregates, coarse sand, gravel, and sea spray

# Medium-size particles - in the range 1 to 100 μm
# sedimentation velocities greater than 0.2 m/s
# settles out slowly
# includes fine ice crystals, pollen, hair, large bacteria, windblown dust, fly ash, coal dust, silt, fine sand, and small dust

# Small particles - less than 1 μm
# falls slowly, take days to years to settle out of a quiet atmosphere. In a turbulent atmosphere they may never settle out
# can be washed out by water or rain
# includes viruses, small bacteria, metallurgical fumes, soot, oil smoke, tobacco smoke, clay, and fumes


######
# The micrometre (International spelling as used by the International Bureau of Weights and Measures;
# SI symbol: μm) or micrometer (American spelling), also commonly known as a micron, 
# is an SI derived unit of length equaling 1×10−6 metre (SI standard prefix "micro-" = 10−6); 
# that is, one millionth of a metre (or one thousandth of a millimetre, 0.001 mm, or about 0.000039 inch).

###### Particle Size Discrimination by PPD42NJ (January 29th, 2013)
# https://i.publiclab.org/system/images/photos/000/010/160/original/Size_Discrimination%28PPD42NJ%29.pdf
#
# Discrimination of particle size can be done using a special method with our Particle Sensor, Model
# PPD42NJ.
#
# PPD42NJ has dual pulse output which works as follows;
# 1) Receptor receives scattered light from the particle, as a pulse.
# 2) Each raw pulse is amplified by an op-amp so that pulse can be acknowledged clearly.
# 3) PPD42NJ has 2 fixed threshold; voltage = 1V for P1 and voltage = 2.5V for P2.
# The threshold represents detecting size of particles, (approx) 1 micron or larger, and (approx.) 2.5
# micron or larger sized particles respectively.
# 
# With PPD42NJ you can read each selected pulse, selected with 2 threshold detection voltage 1V and
# 2.5V which was converted to Lo Pulse directly at the same time.
#
# PPD42NJ also has a port enabling the user to set the alternative threshold detection voltage directly.
# (In other words, a threshold detection voltage 2.5V will be replaced with your designated alternative
# voltage.)

# As you may understand from above 3), you can have 2 different minimum size particles which will
# generate a pulse.
#
# For example:
# Particle sizes of cigarette smoke range from 0.01 micron to around 1micron.
# Particle sizes of house dust range from 1 micron to around 10 micron.
# 
# When you use 1V threshold (when you read Lo Pulse output at P1,) PPD42NJ detects particles
# larger than (approx.) 1 micron.
# 
# When you use 2.5V threshold (when you read Lo Pulse output at P2,) PPD42NJ detects partic#les
# larger than (apporx.) 2.5 micron.
#
# Over 1 micron sized particles represents cigarette smoke and house dust.
#
# Over 2.5 micron sized particles represents house dust only, because this is over the size range of
# cigarette smoke particles
#
# When you use our PPD42NJ to check unidentified particles in the room, you check the Lo Pulse
# occupancy time (ratio) over a certain unit time at both P1 and P2.
#
# By simple math you can then determine how much of which range of particle sizes there are.
#
# Pattern A
# 1V threshold Lo pulse output occupancy ratio : high
# 2.5V threshold Lo pulse output occupancy ratio : low or none
# means you have cigarette smoke at that period.
#
# Pattern B
# 1V threshold Lo pulse output occupancy ratio : high -- (a)
# 2.5V threshold Lo pulse output occupancy ratio : high --(b)
# (a) - k*(b) nearly equal 0(zero)
# means you have house dust at that period
#
# Pattern C
# 1V threshold Lo pulse output occupancy ratio : high -- (a)
# 2.5V threshold Lo pulse output occupancy ratio : high --(b)
# (a) - k*(b) still rather high
# means you have cigarette smoke and house dust at the same time at that period
	
####### Instructions ########################
# On the Raspbery Pi make sure to install pigpio using Apt
# $ sudo apt-get install pigpio python-pigpio python3-pigpio
#
# Once installed make sure to run the pidpio daemon before
# running this script
#
# $ sudo pigpiod
# $ python3 pidustbme680.py
#
# Other packages to install for storing the data and presenting graph data
# $ sudo apt-get install python python3 python3-matplotlib python-matplotlib python3-flask python-flask python3-numpy python-numpy nano git lighttpd sqlite3 sqlite3-dev

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



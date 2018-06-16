#!/usr/bin/env python

# PPD42NS.py
# 2015-11-22
# Public Domain

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
   s = PPD42NS.sensor(pi, 24) 

   with open('airqualitylog.csv', 'w', newline='') as f:
      data_writer = writer(f)
      #write header for csv log file
      data_writer.writerow(['GPIO','Date Time Stamp', 'Ratio', 'Concentration (PCS  per 0.01 cubic foot)'])
   
      while True:

         time.sleep(30) # Use 30 for a properly calibrated reading.

         # Read the values from the sensor
         g, r, c = s.read()
         # Store values in a variable using imperial measures
         imperialdata = g, timestamp, r, int(c)
         
         # Store values in CSV log file
         data_writer.writerow(imperialdata) 
         
         # Print imperial values to console
         print("gpio={} timestamp={} ratio={:.1f} conc={} pcs per 0.01 cubic foot".
            format(g, timestamp, r, int(c)))

   pi.stop() # Disconnect from Pi.


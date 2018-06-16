#!/usr/bin/env python

# PPD42NS.py
# 2015-11-22
# Public Domain

import pigpio

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

   import time
   import pigpio
   import PPD42NS

   pi = pigpio.pi() # Connect to Pi.

   s = PPD42NS.sensor(pi, 24)

   while True:

      time.sleep(1) # Use 30 for a properly calibrated reading.

      g, r, c = s.read()

      print("gpio={} ratio={:.1f} conc={} pcs per 0.01 cubic foot".
         format(g, r, int(c)))

   pi.stop() # Disconnect from Pi.


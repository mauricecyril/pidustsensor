# pidustsensor
Air Quality Monitor using the GROVE / Shinyei PPD42NS dust sensor and the Raspberry Pi 

## Pin Layout

      +-----------------------------------------+
      |                                         |
      |  Shinyei PPD42  / Grove Dust Sensor     |
      |  (Sensor facing you)                    |           
      |                                         |
      |    |+|        |+|                       |          
      |    SL2 POT    CN1 POT                   |
      +-----------------------------------------+
      |    Pin Number                           |
      |                                         |          
      |     |     |     |     |     |           |
      |     5     4     3     2     1           |       
      |     |     |     |     |     |           |
      +-----------------------------------------+
            |     |     |     |     | 
            |     |     |     |  GND (Black)
            |     |     |     |     | 
            |     |  5V (Red) |     | 
            |     |     |     |     | 
            |   PM2.5   |     |     |
            |     |     |     |     | 
            |     |     |   PM1.0   |
            |     |     |     |     |
       Threshold  |     |     |     |
       for Pin 2  |     |     |     | 
            |     |     |     |     | 
            |     |     |     |     | 
 
            

CN : S5B-EH(JST)

1 : COMMON(GND) [Black Wire on Grove Sensor]

2 : OUTPUT(P2) [Not used on Grove Connectr] [Can be used for PM1.0]

3 : INPUT(5VDC 90mA) [Red Wire on Grove Sensor]

4 : OUTPUT(P1) [Yellow Wire on Grove Sensor] [Used for PM2.5 mesurements]

5 : INPUT(T1)･･･FOR THRESHOLD FOR [P2] [Not used on Grove Connector]




# References: 

http://wiki.seeedstudio.com/Grove-Dust_Sensor/ 

https://github.com/Seeed-Studio/Grove_Dust_Sensor

https://indiaairquality.com/2014/12/14/building-pickle-jr-the-low-cost-networked-pm2-5-monitor-part-2/ 

https://indiaairquality.com/2014/12/14/measuring-the-pickle-jr-a-modified-ppd42-with-an-attached-fan/ 

http://irq5.io/2013/07/24/testing-the-shinyei-ppd42ns/ 

http://www.howmuchsnow.com/arduino/airquality/grovedust/

https://github.com/MattSchroyer/DustDuino


## Some direction on how to get the sensor running on a Raspberry Pi 

https://github.com/DexterInd/GrovePi 

https://www.raspberrypi.org/forums/viewtopic.php?t=122298 

https://github.com/DexterInd/GrovePi/blob/master/Software/Python/grove_dust_sensor.py


https://github.com/otonchev/grove_dust 

https://andypi.co.uk/2016/08/19/weather-monitoring-part-2-air-quality-sensing-with-shinyei-ppd42ns/


## Some good reference on how to calculate readings using the pi: 

### Research Paper (2010) from Drexel University, "Air Quality Sensor Network for Philadelphia" by Justin Arling, Kyle O'Connor and Michael Mercieca
http://www.fijnstofmeter.com/documentatie/Data-Validation.pdf

#### These assumptions for calculations are noted as follows:

• All particles are spherical, with a density of 1.65E12 μg/m3

• The radius of a particle in the PM2.5 channel is 0.44 μm

• The radius of a particle in the PM10 channel is 2.60 μm

• 0.01 ft3 can be converted to m3 by multiplying by 3531.5


With the radius of both particle types known, it is possible to derive the volume and multiply by the particle density. This calculation results in the following approximations of mass for each particle type:

• The mass of a particle in the PM2.5 channel is 5.89E-7 μg

• The mass of a particle in the PM10 channel is 1.21E-4 μg

Finally, the following equation will convert the number particles per 0.01 cubic feet to the number of micrograms per cubic meter and the results can be directly compared with other EPA data:

𝑃𝑀 𝐶𝑜𝑛𝑐𝑒𝑛𝑡𝑟𝑎𝑡𝑖𝑜𝑛 (𝜇𝑔/𝑚3) = 𝑁𝑢𝑚𝑏𝑒𝑟 𝑜𝑓 𝑃𝑎𝑟𝑡𝑖𝑐𝑙𝑒𝑠 × 3531.5 × 𝑃𝑎𝑟𝑡𝑖𝑐𝑙𝑒 𝑀𝑎𝑠s


#### Correction factors:

Humidity Correction Table

Humidity [%]	|Dry Correction	|Rain Correction
------------------|-----------------|-------------------
0-19	            |10.1	            |6.4
20-24	            |8.75	            |6.4
25-29	            |8	            |6.4
30-34	            |8	            |6.4
35-39	            |8	            |6.4
40-44	            |7	            |6.3
45-49	            |6	            |6.3
50-54	            |5.75	            |5.7
55-59	            |5.5	            |5.5
60-64	            |5.5	            |4.2
65-69	            |3.5	            |4.1
70-74	            |3.5	            |3.2
75-79	            |3.75	            |3.2
80-84	            |2.25	            |2.1
85-89	            |1.5	            |2.1
90-94	            |0.825	      |0.8
95-100	      |0.525	      |0.5


http://www.fijnstofmeter.com/documentatie/Dylos-conversion.pdf

#### Some conversion algorithms from a dylos air quality sensor:
http://www.fijnstofmeter.com/documentatie/Dylos-Conversion-Sheet.xlsx

Sheet contains the following alorithm "=($B2*3531.5*(5.89*10^-7)*$F$7*$F$8)"

(Particle Count #) * 3531.5 * (5.89*10^-7) * ((Humidity %) * (Dry or Rain Correction))

#### Other references for calculations and using the sensor on the raspberry pi
http://abyz.co.uk/rpi/pigpio/examples.html 

https://github.com/andy-pi/weather-monitor/blob/master/air_quality.py 

https://github.com/andy-pi/weather-monitor/blob/master/pigpio.py


================================================================


# For visualization

https://www.fullstackpython.com/bokeh.html

https://www.fullstackpython.com/blog/responsive-bar-charts-bokeh-flask-python-3.html

https://www.fullstackpython.com/green-unicorn-gunicorn.html



================================================================


## For information on how to use both the PM2.5 and the PM1.0 lines on the sensor see:

http://aqicn.org/api/shinyei/

https://github.com/aqicn/shinyei-lpo

https://github.com/aqicn/shinyei-lpo/blob/master/shinyei-lpo-reader.py


http://aqicn.org/faq/2013-02-02/why-is-pm25-often-higher-than-pm10/


## Arduino specific but can be used to get calculations

https://github.com/MattSchroyer/DustDuino/blob/master/DustDuino.ino

https://github.com/MattSchroyer/DustDuino/blob/master/DustDuinoSerial.ino


For how to contribute to World Air Quality Index

http://aqicn.org/api/sensor/



=================================================================


## Calculations used on PI

            ratio = float(self._low_ticks)/float(interval)*100.0
            conc = 1.1*pow(ratio,3)-3.8*pow(ratio,2)+520*ratio+0.62;
            

## Calculations used on Arduino
https://github.com/MattSchroyer/DustDuino/blob/master/DustDuinoSerial.ino

      // Generates PM10 and PM2.5 count from LPO.
      // Derived from code created by Chris Nafis
      // http://www.howmuchsnow.com/arduino/airquality/grovedust/

      ratioP1 = durationP1/(sampletime_ms*10.0);  // Integer percentage 0=>100
      ratioP2 = durationP2/(sampletime_ms*10.0);
      countP1 = 1.1*pow(ratioP1,3)-3.8*pow(ratioP1,2)+520*ratioP1+0.62;
      countP2 = 1.1*pow(ratioP2,3)-3.8*pow(ratioP2,2)+520*ratioP2+0.62;
      float PM10count = countP2;
      float PM25count = countP1 - countP2;


      // Assues density, shape, and size of dust
      // to estimate mass concentration from particle
      // count. This method was described in a 2009
      // paper by Uva, M., Falcone, R., McClellan, A.,
      // and Ostapowicz, E.
      // http://wireless.ece.drexel.edu/research/sd_air_quality.pdf
      
      // first, PM10 count to mass concentration conversion
      double r10 = 2.6*pow(10,-6);
      double pi = 3.14159;
      double vol10 = (4.0/3.0)*pi*pow(r10,3);
      double density = 1.65*pow(10,12);
      double mass10 = density*vol10;
      double K = 3531.5;
      float concLarge = (PM10count)*K*mass10;
      
      // next, PM2.5 count to mass concentration conversion
      double r25 = 0.44*pow(10,-6);
      double vol25 = (4.0/3.0)*pi*pow(r25,3);
      double mass25 = density*vol25;
      float concSmall = (PM25count)*K*mass25;



=================================================================

# Wiring

One method is to use the wiriing method using a voltage divider described by 
https://github.com/otonchev/grove_dust 
The Shinyei sensor is connected to the GPIO on the Raspberry Pi in the following
manner:


          +------------------+
          |                  |
          |  Shinyei PPD42   |
          |                  |
          +------------------+
            |      |       |
            | black|       |yellow          _____
         red|      |       +---------------[_____]-----+
            |      |                         2kOm      |
            |      |               _____               |
            |      +--------+-----[_____]--------------+
            |               |       3kOm               |
            *               *                          *
       GPIOPin2(5V)    GPIOPin6(GND)             GPIOPin11(17)


Another method is to use a bi-directional logicl level converter that allows you to use a 5v sensor with the 3.3v on the Pi GPIO pins.

https://learn.sparkfun.com/tutorials/bi-directional-logic-level-converter-hookup-guide

https://www.adafruit.com/product/757


      +-----------------------------------------+
      |                                         |
      |  Shinyei PPD42  / Grove Dust Sensor     |
      |  (Sensor facing you)                    |           
      |                                         |
      |    |+|        |+|                       |          
      |    SL2 POT    CN1 POT                   |
      +-----------------------------------------+
      |    Pin Number                           |
      |                                         |          
      |     |     |     |     |     |           |
      |     5     4     3     2     1           |       
      |     |     |     |     |     |           |
      +-----------------------------------------+
            |     |     |     |     | 
            |     |     |     |  GND (Black)
            |     |     |     |     | 
            |     |  5V (Red) |     | 
            |     |     |     |     | 
            |   PM2.5   |     |     |
            |     |     |     |     |                 +-----------------------+
            |     |     |   PM1.0   |                 |Bi-Direction Logic     |
            |     |     |     |     |                 |Level Converter        |
            |     |     |     |     |                 +-----------------------+
       Threshold  |     |     |     +--(1) GND--------|  GND              GND |----[[RPi GND Pin]]
       for Pin 2  |     |     |                       |                       |
            |     |     |     +-----(2) PM1.0---------|  B1               A1  |----[[RPi GPIO Pin]]
            |     |     |                             |                       |
            |     |     +-----------(3) 5V------+-----|  HV               LV  |----[[RPi 3.3V Pin]]
            |     |                             |     |                       |
            |     |                             |     |                       |
            |     |             [[RPi 5V Pin]]--+     |                       |
            |     |                                   |                       |
            |     +-----------------(4) PM2.5---------|  B2               A2  |----[[RPi GPIO Pin]]
            |                                         +-----------------------+
            |
       [[Not used]]


Third option is to Pi Hat or Phat like the Pirimoni's Envirohat 
https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-enviro-phat however this might still require a voltage divider: 
https://learn.pimoroni.com/static/repos/learn/sandyj/enviro_phat_voltage_divider.png
Warning: Use a voltage divider at your own risk.


      +-----------------------------------------+
      |                                         |
      |  Shinyei PPD42  / Grove Dust Sensor     |
      |  (Sensor facing you)                    |           
      |                                         |
      |    |+|        |+|                       |          
      |    SL2 POT    CN1 POT                   |
      +-----------------------------------------+
      |    Pin Number                           |
      |                                         |          
      |     |     |     |     |     |           |
      |     5     4     3     2     1           |       
      |     |     |     |     |     |           |
      +-----------------------------------------+
            |     |     |     |     | 
            |     |     |     |  GND (Black)
            |     |     |     |     | 
            |     |  5V (Red) |     | 
            |     |     |     |     | 
            |   PM2.5   |     |     |
            |     |     |     |     | 
            |     |     |   PM1.0   |
            |     |     |     |     |     1 kΩ        1 kΩ resistor
       Threshold  |     |     |     +----[_____]-----[_____]------+--------> [[Pi GND Pin]]
       for Pin 2  |     |     |                                   |
            |     |     |     |                  1 kΩ resistor    |
            |     |     |     +----------------[_____]------------+--------> [[Pi GPIO Pin 7]]
            |     |     |                                         |
            |     |     +-----------------> [[Pi 5V Pin]]         |
            |     |                                               |
            |     |                              1 kΩ resistor    |
            |     +----------------------------[_____]------------+--------> [[Pi GPIO Pin 8]]
            |
            |
       [[Not used]]

# pidustsensor
Air Quality Monitor using the GROVE / Shinyei PPD42NS dust sensor and the Raspberry Pi

References: 
http://wiki.seeedstudio.com/Grove-Dust_Sensor/ 
https://github.com/Seeed-Studio/Grove_Dust_Sensor

https://indiaairquality.com/2014/12/14/building-pickle-jr-the-low-cost-networked-pm2-5-monitor-part-2/ 
https://indiaairquality.com/2014/12/14/measuring-the-pickle-jr-a-modified-ppd42-with-an-attached-fan/ 
http://irq5.io/2013/07/24/testing-the-shinyei-ppd42ns/ 
http://www.howmuchsnow.com/arduino/airquality/grovedust/
https://github.com/MattSchroyer/DustDuino


Some direction on how to get the sensor running on a Raspberry Pi 
https://github.com/DexterInd/GrovePi 
https://www.raspberrypi.org/forums/viewtopic.php?t=122298 
https://github.com/DexterInd/GrovePi/blob/master/Software/Python/grove_dust_sensor.py

https://github.com/otonchev/grove_dust 
https://andypi.co.uk/2016/08/19/weather-monitoring-part-2-air-quality-sensing-with-shinyei-ppd42ns/

Some good reference on how to calculate readings using the pi and the primary source of where we'll be attempting to use the onion omega platform instead of the raspberry pi. 
http://abyz.co.uk/rpi/pigpio/examples.html 
https://github.com/andy-pi/weather-monitor/blob/master/air_quality.py 
https://github.com/andy-pi/weather-monitor/blob/master/pigpio.py

================================================================

For visualization
https://www.fullstackpython.com/bokeh.html
https://www.fullstackpython.com/blog/responsive-bar-charts-bokeh-flask-python-3.html
https://www.fullstackpython.com/green-unicorn-gunicorn.html


================================================================

For information on how to use both the PM2.5 and the PM1.0 lines on the sensor see:
http://aqicn.org/api/shinyei/
https://github.com/aqicn/shinyei-lpo
https://github.com/aqicn/shinyei-lpo/blob/master/shinyei-lpo-reader.py

http://aqicn.org/faq/2013-02-02/why-is-pm25-often-higher-than-pm10/

Arduino specific but can be used to get calculations
https://github.com/MattSchroyer/DustDuino/blob/master/DustDuino.ino
https://github.com/MattSchroyer/DustDuino/blob/master/DustDuinoSerial.ino



For how to contribute to World Air Quality Index
http://aqicn.org/api/sensor/


=================================================================
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


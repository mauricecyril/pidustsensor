#!/usr/bin/env python

# sendarduinoserialtoadafruitio.py

from datetime import datetime
from Adafruit_IO import Client, RequestError, Feed
import time
import sys
import serial
import sendarduinoserialtoadafruitio.py


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

io_LPO = aio.feeds('environment-sensor.ardlpo')
io_RATIO = aio.feeds('environment-sensor.ardratio')
io_CONC = aio.feeds('environment-sensor.artconc')


# Setup Serial Connection
ser = serial.Serial('/dev/tty.usbserial', 9600)


# Read Serial and Parse infomation to Adafruit

# Start Loop
while True:
    timestamp = datetime.now()

    # Print Serial Readings to console
    print(timestamp + " - " ser.readline())
    print(ser.split(',')


    # Split serial reading and assign to a list
    serlist = ser.split(',')
    
    # Print List
    print (serlist[0])

    print (serlist[1])

    print (serlist[2])

    # Assign each list item to a variable

    # Assign first list item to Grove Dust Sensor LPO reading
    ardlpo = serlist[0]

    # Assign first list item to Grove Dust Sensor Ratio reading
    ardratio = serlist[1]

    # Assign first list item to Grove Dust Sensor concentration reading
    ardconc = serlist[2]
    

    # Send information to Adafruit IO
    # Send values to ADAFRUIT.IO or Pass if there's connection error
    try:
        aio.send_data(io_LPO.key, ardlpo)
        aio.send_data(io_RATIO.key, ardratio)
        aio.send_data(io_CONC.key, ardconc)

    except ConnectionError:
        pass
    except MaxRetryError:
        pass
    except BrokenPipeError:
        pass
    except ConnectionAbortedError:
        pass
    except ConnectionRefusedError:
        pass
    except ConnectionResetError:
        pass
    except TimeoutError:
        pass

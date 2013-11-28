#!/usr/bin/python
#
# TSCU Weather Node script - based on AdaFruit demo code and modified by Jeff Tarr 26-Nov-2013

import subprocess
import re
import sys
import time
import datetime
import gspread
import RPi.GPIO as GPIO
from Adafruit_BMP085 import BMP085
import gps
from config import *

# Setup LEDs
GPIO.setmode(GPIO.BCM)
GREEN_LED = 23
RED_LED = 18
GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.setup(RED_LED, GPIO.OUT)
GPIO.output(GREEN_LED, False)
GPIO.output(RED_LED, True)

# Setup BMP pressure sensor
bmp = BMP085(0x77)

# Setup GPS sensor
gpssession = gps.gps("localhost", "2947")
gpssession.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

# Login with your Google account
try:
  gc = gspread.login(email, password)
except:
  print "Unable to log in.  Check your email address/password"
  sys.exit()

# Open a worksheet from your spreadsheet using the filename
try:
  worksheet = gc.open(spreadsheet).sheet1
  # Alternatively, open a spreadsheet using the spreadsheet's key
  #worksheet = gc.open_by_key('0AldnNT5XbvdpPYRGUHZUcnd5ZHVTOUx5N0VYQUE')
except:
  print "Unable to open the spreadsheet.  Check your filename: %s" % spreadsheet
  sys.exit()

# Continuously append data
while(True):
  try:
	report = gpssession.next()
	print report
  except KeyError:
	pass
  except KeyboardInterrupt:
	quit()
  except StopIteration:
	gpssession= None
	print "GPSD has terminated"


  output = subprocess.check_output(["./Adafruit_DHT", "2302", "4"]);

  matches = re.search("Temp =\s+([0-9.]+)", output)
  if (not matches):
	time.sleep(3)
	continue
  
  temp = float(matches.group(1)) * 9/5 + 32
   
  # search for humidity printout
  matches = re.search("Hum =\s+([0-9.]+)", output)
  if (not matches):
	time.sleep(3)
	continue
  humidity = float(matches.group(1))

  print "Temperature: %.1f F" % temp
  print "Humidity:    %.1f %%" % humidity

  # Get data from BMP sensor
  bmptemp = bmp.readTemperature() * 9/5 + 32
  bmppressure = bmp.readPressure() 
  bmpaltitude = bmp.readAltitude(bmppressure)
  bmppressure = bmppressure / 100.0

  print "BPM Temperature %.2f F" % bmptemp
  print "BPM Pressure %.2f hPa" % bmppressure
  print "BPM Altitude %.2f" % bmpaltitude

  # Get data from GPS
  # This is coming...

  gpsaltitude = 100
  gpslatitude = 40.803775
  gpslongitude = -73.966282
  gpsvisiblesats = 20

  # Append the data in the spreadsheet, including a timestamp
  try:
    values = [datetime.datetime.now(), temp, humidity, bmppressure, bmptemp, bmpaltitude, gpslatitude, gpslongitude, gpsaltitude, gpsvisiblesats]
    worksheet.append_row(values)
  except:
    print "Unable to append data.  Check your connection?"
    sys.exit()

  # Wait 30 seconds before continuing
  print "Posted: ",
  print (values)
  time.sleep(60)

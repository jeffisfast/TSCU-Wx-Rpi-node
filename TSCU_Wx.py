#!/usr/bin/python
#
# TSCU Weather Node script - based on AdaFruit demo code and modified by Jeff Tarr 26-Nov-2013

import os
import glob
import subprocess
import re
import sys
import time
import datetime
import gspread
from Adafruit_BMP085 import BMP085
from config import *

# Setup DS18B20 sensor
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
 
def read_temp_raw():
	catdata = subprocess.Popen(['cat',device_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out,err = catdata.communicate()
	out_decode = out.decode('utf-8')
	lines = out_decode.split('\n')
	return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

# Setup BMP pressure sensor
bmp = BMP085(0x77)

# Continuously append data
while(True):
  # Login with your Google account
  try:
    gc = gspread.login(email, password)
  except:
    print "Unable to log in.  Check your email address/password"

  output = subprocess.check_output(["./Adafruit_DHT", "2302", "22"]);

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

  print "2302 Temperature: %.1f F" % temp
  print "2302 Humidity:    %.1f %%" % humidity

  deg_c, deg_f = read_temp()

  print "28 Temperature: %.1f F" % deg_f

  # Get data from BMP sensor
  bmptemp = bmp.readTemperature() * 9/5 + 32
  bmppressure = bmp.readPressure() 
  bmpaltitude = bmp.readAltitude(bmppressure)
  bmppressure = bmppressure / 100.0

  print "BPM Temperature %.2f F" % bmptemp
  print "BPM Pressure %.2f hPa" % bmppressure
  print "BPM Altitude %.2f" % bmpaltitude


  # Append the data in the spreadsheet, including a timestamp
  try:
    worksheet = gc.open(spreadsheet).sheet1
    values = [datetime.datetime.now(), temp, humidity, bmppressure, bmptemp, bmpaltitude, deg_f]
    worksheet.append_row(values)

  except:
    print "Unable to append data.  Check your connection?"

  # Wait 60 seconds before continuing
  print "Posted: ",
  print (values)
  time.sleep(60)

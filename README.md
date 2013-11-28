TSCU-Wx-Rpi-node
================

TSCU class project to monitor weather using a Raspberry Pi.  Watch this space for more information.

Basic setup information:

1. Raspberry PI with 2302 temperature & humidity sensor, Ultimate GPS chip, and BMP pressure sensor.
2. Install the Adafruit Raspberry PI python demo code and follow their instructions for building the C libraries for faster processing times.
3. Install the I2C stuff from Adafruit too.
4. Install this git tree.
5. Make symbolic links to Adafruit_BMP085.py, Adafruit_DHT, Adafruit_I2C.py as appropriate for your install locations.
6. Copy the config_example.py file to config.py and edit it to match your Google credentials.
7. Use "sudo python TSCU_Wx.py" to run the code. 

#!/usr/bin/python
################################################################################################
# Name: 		Sensor
#
# Beschreibung:	Ermittelt die Sensordaten Temperatur, Luftfeuchtigkeit, Luftdruck, Bodenfeuchtigkeit
#				mit dem GrovePi+ und RaspberryPi B+
# Author: 		Dogcrafter
# Author URI: 	https://blog.dogcrafter.de
# License: 		GPL2
# License URI: 	http://www.gnu.org/licenses/gpl-2.0.html
################################################################################################
import subprocess 
import grovepi
import smbus
from libs.grove_barometic_sensor import BMP085

class Sensor():
	global bmp
	global bus
	global dht_sensor_port
	global tem_correction
	global moist_sensor_port
	dht_sensor_port = 7		# Connect the DHt sensor to port D7
	temp_correction = - 0.5   # correction of measured temperature
	moist_sensor_port = 0   # Connect the Moisture sensor to port A0
	bmp = BMP085(0x77, 1)
	bus = smbus.SMBus(1)    # I2C 1
	
	def getList(self):
		return self.sensor
	def getBTempData(self):
		btemp = bmp.readTemperature()
		print "Barometer Temperatur = %.2f C" % btemp
		return btemp 
	def getPressData(self):
		pressure = bmp.readPressure()/100   # /100 -> hPa
		# sensor counts sometimes data above 1200 hPa
		while pressure > 1200:
			pressure = bmp.readPressure()/100   # /100 -> hPa
		print "Luftdruck            = %.2f hPa" % pressure
		return pressure
	def getAltData(self):
		altitude = bmp.readAltitude(102000)
		print "Hoehe                = %.2f m" % altitude
		return altitude
	def getMoistData(self):
		#moist = grovepi.analogRead(moist_sensor_port)
		print "Boden Feuchte        = %.2f " % 0
		return 0
	def getHumData(self):
		[ temp,hum ] = grovepi.dht(dht_sensor_port,3)
		print "rel Feuchte          = %.2f " % hum
		return hum
	def getTempData(self):
		[ temp,hum ] = grovepi.dht(dht_sensor_port,3)
		print "Temperatur           = %.2f C" % temp
		return temp		
	

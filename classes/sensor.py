#!/usr/bin/python
################################################################################################
# Name: 		Sensor
#
# Beschreibung:	Ermittelt die Sensordaten Temperatur, Luftfeuchtigkeit, Luftdruck, Bodenfeuchtigkeit
#				mit dem GrovePi+ und RaspberryPi B+
# Version: 		1.0.0
# Author: 		Stefan Mayer
# Author URI: 	http://www.2komma5.org
# License: 		GPL2
# License URI: 	http://www.gnu.org/licenses/gpl-2.0.html
################################################################################################
# Changelog 
# 1.0.0 - 	Initial release
#
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
		return btemp 
	def getPressData(self):
		pressure = bmp.readPressure()/100   # /100 -> hPa
		return pressure
	def getAltData(self):
		altitude = bmp.readAltitude(102000)
		return altitude
	def getMoistData(self):
		#moist = grovepi.analogRead(moist_sensor_port)
		return 0
	def getHumData(self):
		[ temp,hum ] = grovepi.dht(dht_sensor_port,3)
		return hum
	def getTempData(self):
		[ temp,hum ] = grovepi.dht(dht_sensor_port,3)
		return temp		

	

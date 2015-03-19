#!/usr/bin/python
import subprocess 
import re 
import os 
import sys 
import time 
import grovepi
import smbus
from grove_barometic_sensor import BMP085


class Weather():
	global bmp
	global bus
	global backupFileLocationPress
	global backupFileLocationTrend
	global dht_sensor_port
	global tem_correction
	global moist_sensor_port
	
	dht_sensor_port = 7		# Connect the DHt sensor to port D7
	temp_correction = - 0.5   # correction of measured temperature
	moist_sensor_port = 0   # Connect the Moisture sensor to port A0
	bmp = BMP085(0x77, 1)
	bus = smbus.SMBus(1)    # I2C 1
	backupFileLocationPress="/home/pi/Wurmfarm/dataPressure.txt"
	backupFileLocationTrend="/home/pi/Wurmfarm/dataTrend.txt"

	def init(self):
		self.press = []
		i = 0
		press = self.getPressData()
		self.trendPress = self.getPressData()
		while i < 12:
			self.addPress(press)
			i = i + 1
		self.actTrend = 1	
		self.savePressToFile()
		self.actTrend = 3	
		self.saveTrendToFile()
		
	def __init__(self):
		#("Gewitter")			#12
		#("Regen")		 		#0
		#("vereinzelt Regen") 	#1
		#("wechselhaft")     	#2
		#("bedeckt")			#3
		#("bewoelkt")		 	#4
		#("heiter")		     	#5
		#("sonnig")			 	#6
		
		if ((True == self.is_non_zero_file(backupFileLocationPress)) and (True == self.is_non_zero_file(backupFileLocationTrend))): 
			self.checkPress()
		else: 
			self.init()
			
		
	def is_non_zero_file(self,fpath):  
		return True if os.path.isfile(fpath) and os.path.getsize(fpath) > 0 else False
	def checkPress(self):
		file = open(backupFileLocationPress, 'r')
		for lines in file:
			items        = []
			items        = lines.split()
		file.close	
		actPress = self.getPressData()
		oldPress = int(items[0])
		deltaPress = actPress - oldPress
		#print actPress, "-", oldPress,"=",deltaPress
		if ( deltaPress <= -5 ):
			items[11] = actPress
			self.press = []
			i = 0
			while i < 11:
				items[i] = items[i+1]
				i = i + 1
			i = 0
			while i < 12:
				self.addPress(items[i])
				i = i + 1
			self.savePressToFile()
			return 12
		else:
			return self.checkTrend()
	def checkTrend(self):		
		file = open(backupFileLocationTrend, 'r')
		for lines in file:
			items        = []
			items        = lines.split()
		file.close	
		actPress = self.getPressData()
		actTrend = int(items[0])
		oldPress = int(items[1])
		deltaPress = actPress - oldPress
		#print actTrend, actPress, "-", oldPress,"=",deltaPress
		if (deltaPress >= 3):
			if (actTrend <> 6):
				self.actTrend = actTrend + 1
			self.trendPress = actPress
			self.saveTrendToFile()
			return self.actTrend
		if (deltaPress <= -3):
			if (actTrend <> 0):
				self.actTrend = actTrend - 1
			self.trendPress = actPress
			self.saveTrendToFile()
			return self.actTrend
		if (deltaPress > - 3 and deltaPress < 3 ):
			return actTrend			
		
	def addPress(self,press):
		self.press.append(press)
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
	def savePressToFile(self):
		file = open(backupFileLocationPress, 'w')
		for press in self.press:
			data = str(press) + " "
			file.write(data)
		file.close 
	def saveTrendToFile(self):
		file = open(backupFileLocationTrend, 'w')
		data = str(self.actTrend) + " " + str(self.trendPress)
		file.write(data) 
		file.close
	def getDewPoint(self):
		temp = self.getTempData()
		hum = self.getHumData()/100
		dewPoint = ((109.8 + temp )*(hum**(1/8.02))) - 109.8
		return dewPoint




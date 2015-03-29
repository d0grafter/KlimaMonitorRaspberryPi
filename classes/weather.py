#!/usr/bin/python
################################################################################################
# Name: 		Wetter
#
# Beschreibung:	Berechnet eine Wettervorhersage
# Version: 		1.0.1
# Author: 		Stefan Mayer
# Author URI: 	http://www.2komma5.org
# License: 		GPL2
# License URI: 	http://www.gnu.org/licenses/gpl-2.0.html
################################################################################################
# Changelog 
# 1.0.0 - 	Initial release
# 1.0.1 -	Auslagerung der Sensordatenermittlung in eigene Klasse
#			Speicherung der Daten im JSON-Format
################################################################################################
import subprocess 
import re 
import os 
import sys 
import time 
import smbus
import math
import json
from sensor import Sensor

#Gewitter 			#-1
#Regen		 		#0
#vereinzelt Regen	#1
#wechselhaft		#2
#bedeckt			#3
#bewoelkt 			#4
#heiter    			#5
#sonnig 			#6
	
class Weather():
	global JSON_File
	global forecast_trend
	global forecast_max
	global forecast_min
	global forecast_storm
	forecast_trend = 3
	forecast_max = 6
	forecast_min = 0
	forecast_storm = -5
	path = os.path.dirname(os.path.abspath(sys.argv[0]))
	JSON_File = path + "/files/forecast.json"

	def init(self):
		press = self.sensorInst.getPressData()
		data = {"forecast": { "pressure": press, "trend": 3},"stormwarning":{"pressure": [press,press,press,press,press,press,press,press,press,press,press,press],"deltaPressure":0}}
		print "Weather Init"
		self.saveJSONData(data)
		
	def __init__(self):
		self.sensorInst = Sensor()		
		if (False == self.is_non_zero_file(JSON_File)): 
			self.init()
	
	def is_non_zero_file(self,fpath):  
		return True if os.path.isfile(fpath) and os.path.getsize(fpath) > 0 else False
	def checkForecast(self):
		data = self.readJSONData()
		# Sturm Warnung bei abfall von mehr als forecast_storm hPa
		data = self.checkPress(data)
		if ( data["stormwarning"]["deltaPressure"] <= forecast_storm ):
			self.saveJSONData(data)
			return -1
		else:
			data = self.checkTrend(data)
			self.saveJSONData(data)
			return data["forecast"]["trend"] 
		
	def checkPress(self,data):
		# Speichert und prueft den Luftdruck ueber 6 Stunden
		actPress = self.sensorInst.getPressData()
		oldPress = data["stormwarning"]["pressure"][0]
		deltaPress = actPress - oldPress
		#print actPress, "-", oldPress,"=",deltaPress
		#neuer Wert an letzte Stelle
		i = 0
		# erste stelle loeschen
		while i < 11:
			data["stormwarning"]["pressure"][i] = data["stormwarning"]["pressure"][i+1]
			i = i + 1
		data["stormwarning"]["pressure"][11] = actPress
		data["stormwarning"]["deltaPressure"] = deltaPress
		return data
	def checkTrend(self,data):		
		actPress = self.sensorInst.getPressData()
		actTrend = data["forecast"]["trend"]
		oldPress = data["forecast"]["pressure"]
		deltaPress = actPress - oldPress
		self.deltaPress = deltaPress
		#print actTrend, actPress, "-", oldPress,"=",deltaPress
		if (deltaPress >= forecast_trend):
			if (actTrend <> forecast_max):
				data["forecast"]["trend"] = actTrend + 1
			data["forecast"]["pressure"] = actPress
		if (deltaPress <= -forecast_trend):
			if (actTrend <> forecast_min):
				data["forecast"]["trend"] = actTrend - 1
			data["forecast"]["pressure"] = actPress
		if (deltaPress > -forecast_trend and deltaPress < forecast_trend ):
				data["forecast"]["trend"] = actTrend
		return data

	def getTrend(self):
		if (self.deltaPress == 0):
			return "="
		if	(self.deltaPress > 0):
			return "+"
		if (self.deltaPress < 0):
			return "-"	
	def getDewPoint(self):
		t = self.sensorInst.getTempData()
		relF = self.sensorInst.getHumData()
		# Ortshoehe
		hNN = 114
		pNN = self.sensorInst.getPressData()
		#Luftdruck Ortshoehe
		pO= pNN-(hNN/(8.7 - hNN * 0.0005))
		#Luftdicht
		LD = (0.349 * pO) / (273.15 + t)
		#Saettigungsdampfdruck
		pS= 6.1078 * (10**(t * 7.5/(t + 273.15)))
		#Saettigungsdefizit
		Sd = pS - ((pS/100) * relF)
		#Dampfdruck
		pD = pS - Sd
		#Taupunkt
		TP = (234.67 * (math.log(pD) / math.log(10)) - 184.2) / (8.233 - ( math.log(pD) / (math.log(10))))
		#spez Luftfeuchte gramm/Kubikmeter Luft
		spezF = ((pD/pO)*0.622)*10**3
		self.spezF =spezF* LD
		#Saettigungsfeuchte gramm/Kubikmeter Luft 
		sattF = (spezF/relF)*100
		self.sattF = sattF * LD
		return TP
	def getspezF(self):
		return self.spezF
	def getsattF(self):
		return self.sattF
	def readJSONData(self):
		with open(JSON_File) as data_file:    
			data = json.load(data_file)
		return data
	def saveJSONData(self, data):
		with open(JSON_File, 'w') as outfile:
			json.dump(data, outfile, sort_keys = True, indent = 4, ensure_ascii=False)
		print "Forecast data saved"




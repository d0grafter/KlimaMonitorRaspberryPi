#!/usr/bin/python
################################################################################################
# Name: 		Wetter
#
# Beschreibung:	Berechnet eine Wettervorhersage
# Author: 		Dogcrafter
# Author URI: 	https://blog.dogcrafter.de
# License: 		GPL2
# License URI: 	http://www.gnu.org/licenses/gpl-2.0.html
################################################################################################
import subprocess 
import re 
import os 
import sys 
import time 
import datetime
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
	global trend
	trend = "="
	forecast_trend = 3
	forecast_max = 6
	forecast_min = 0
	forecast_storm = -5
	path = os.path.dirname(os.path.abspath(sys.argv[0]))
	JSON_File = path + "/files/forecast.json"

	def init(self):
		press = self.sensorInst.getPressData()
		timeStamp = str(datetime.datetime.now())
		data = {"saveTime":timeStamp,"Trend": trend, "Forecast": 3,
		"oldForecast": 3, "oldPressure": press,"TrendPressure": press, "Pressure": [press,press,press,press,press,press,press,press,press,press,press,press]}
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
		data = self.checkTrend(data)
		data = self.checkPress(data)
		self.saveJSONData(data)
		return data["Forecast"], data["Trend"] 

	def checkPress(self,data):
		# Speichert und prueft den Luftdruck ueber 6 Stunden
		actPress = self.sensorInst.getPressData()
		oldPress = data["Pressure"][0]
		deltaPress = actPress - oldPress
		print "checkPress: ", actPress, "-", oldPress,"=",deltaPress
		#neuer Wert an letzte Stelle
		i = 0
		# erste stelle loeschen
		while i < 11:
			data["Pressure"][i] = data["Pressure"][i+1]
			i = i + 1
		data["Pressure"][11] = actPress
		# Sturm Warnung bei Abfall von mehr als forecast_storm hPa
		if ( deltaPress <= forecast_storm ):
			data["Forecast"] = -1
		return data
	def checkTrend(self,data):		
		actPress = self.sensorInst.getPressData()
		actForecast = data["Forecast"]
		if (actForecast == -1):
			actForecast = data["oldForecast"]
		oldPress = data["oldPressure"]
		deltaPress = actPress - oldPress
		print "checkTrend: ", actPress, "-", oldPress,"=",deltaPress
		if actForecast < 0:
			actForecast = 0
		if (deltaPress >= forecast_trend):
			if (actForecast <> forecast_max):
				data["Forecast"] = actForecast + 1
			data["oldPressure"] = actPress
		if (deltaPress <= -forecast_trend):
			if (actForecast <> forecast_min):
				data["Forecast"] = actForecast - 1
			data["oldPressure"] = actPress
		if (deltaPress > -forecast_trend and deltaPress < forecast_trend ):
				data["Forecast"] = actForecast
		data["oldForecast"] = data["Forecast"]
		print "Vorhersage           = %.20s " % data["Forecast"]
		# berechne den Trend Luftdruck in einer halben Stunde
		self.calcLinTrend(data)
		trendPress = data["TrendPressure"] 
		deltaPress = trendPress - actPress 
		if (deltaPress == 0):
			data["Trend"] = "="
		if	(deltaPress > 0):
			data["Trend"] = "+"
		if (deltaPress < 0):
			data["Trend"] = "-"
		print "Trend                = %.1s " % data["Trend"]	
		return data

	def calcLinTrend(self,data):
		# y=mx+b, b=y-mx, m=sum(y1-yn)*(x1-xn)/sum(x1-xn)^2
		i = 1
		z = 0
		n = 0
		while i < 12:
			z =  z  + float((data["Pressure"][i-1] - data["Pressure"][i]) * ( i - (i+1)))
			n = n +  float((i - (i+1))**2)
			i = i + 1
		m = float(z/n)
		b = float(data["Pressure"][11] - m * 12)
		y = m * 13 + b
		data["TrendPressure"] = y
		print "kalk. Luftdruck      = %.2f hPa" % y
		return data	
	
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
		print "Taupunkt             = %.2f C" % TP
		return TP
	def getspezF(self):
		print "spez. Feuchte        = %.2f g/m^3" % self.spezF
		return self.spezF
	def getsattF(self):
		print "saett. Feuchte       = %.2f g/m^3" % self.sattF
		return self.sattF
	def readJSONData(self):
		with open(JSON_File) as data_file:    
			data = json.load(data_file)
		return data
	def saveJSONData(self, data):
		timeStamp = datetime.datetime.now()
		data["saveTime"] = str(timeStamp)
		with open(JSON_File, 'w') as outfile:
			json.dump(data, outfile, sort_keys = True, indent = 4, ensure_ascii=False)
		print "Forecast data saved", str(timeStamp)


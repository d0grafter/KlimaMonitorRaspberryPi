#!/usr/bin/python
################################################################################################
# Name: 		Wurmfarm Klima Monitor
#
# Beschreibung:	Ermittelt die Sensordaten Temperatur, Luftfeuchtigkeit, Luftdruck, Bodenfeuchtigkeit
#				mit dem GrovePi+ und uebermittelt diese an die Wordpress Datenbank
# Version: 		1.1.0
# Author: 		Stefan Mayer
# Author URI: 	http://www.2komma5.org
# License: 		GPL2
# License URI: 	http://www.gnu.org/licenses/gpl-2.0.html
################################################################################################
# Changelog 
# 1.0.0 - 	Initial release
# 1.1.0 - 	Speicherung der Sensordatenin lokale Datei, falls keine Datenbankverbindung besteht
#			Nach erneutem Aufbau der Verbindung, werden die Daten aus der lokalen Datei 
#			automatisch in die Datenbank uebernommen
################################################################################################

import subprocess 
import re 
import os 
import sys 
import time 
import MySQLdb as mdb
import datetime
from weather import Weather

databaseUsername="USER"
databasePassword="PASSWORD" 
databaseName="DATABASENAME" 
databaseTable="DATABASETABLENAME"
backupFileLocation="/home/pi/Wurmfarm/dataBackup.txt"

def saveToDataBackup(forecast,trend,temp,hum,moist,btemp,press,alt,dewPoint,spezF,sattF,currentDate,timeStamp):
	file = open(backupFileLocation, 'a')
	data = str(forecast) + " " +  str(trend) + " " + str(temp) + " " + str(hum) + " " + str(btemp) + " " + str(press) + " " + str(alt) + " " + str(moist) + " " + str(dewPoint) + " " + str(spezF) + " " + str(sattF) + " " + str(currentDate) + " " + str(timeStamp) + "\n"
	file.write(data)
	file.close
	return "true"

def getDataBackupToDatabase(dbConnect):
	
	file = open(backupFileLocation, 'r')
	with dbConnect:
		dbCursor = dbConnect.cursor()
		for lines in file:
			items        = []
			items        = lines.split()
			forecast     = items[0]
			trend        = items[1]
			temp         = items[2]
			hum          = items[3]
			btemp        = items[4]
			press        = items[5] 
			alt          = items[6] 
			moist        = items[7] 
			dewPoint     = items[8]
			spezF		 = items[9]
			sattF        = items[10]
			currentDate  = items[11]
			timeStamp    = items[12] + " " + items[13]
			
			dbCursor.execute("INSERT INTO " +  databaseTable + " (forecast,trend, temperature, humidity, btemp, pressure, altitude, moisture,dewPoint,spezF,sattF,dateMeasured, timeStamp) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(forecast,trend,temp,hum,btemp,press,alt,moist,dewPoint,spezF,sattF,currentDate,timeStamp))
			print forecast,trend, temp, hum, btemp,press,alt,moist,dewPoint,spezF,sattF,currentDate, timeStamp
			print "Wrote stored data from local file to database"
	file.close
	file =  open(backupFileLocation, 'w')
	file.close
		
def saveToDatabase(forecast,trend,temp,hum,moist,btemp,press,alt,dewPoint,spezF,sattF,currentDate,timeStamp):

	try:         
		dbConnect=mdb.connect("127.0.0.1", databaseUsername, databasePassword, databaseName)
	except:
		print "Saved data to local file, until the DB connection is back"
		return saveToDataBackup(forecast,trend,temp,hum,moist,btemp,press,alt,dewPoint,spezF,sattF,currentDate,timeStamp)
		
	with dbConnect:
		# first get possible backup data to the database    
		getDataBackupToDatabase(dbConnect)
		dbCursor = dbConnect.cursor()
		dbCursor.execute("INSERT INTO " +  databaseTable + " (forecast,trend,temperature,humidity, btemp, pressure, altitude, moisture,dewPoint,spezF,sattF,dateMeasured, timeStamp) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(forecast,trend,temp,hum,btemp,press,alt,moist,dewPoint,spezF,sattF,currentDate,timeStamp))
		print "Saved data: ", timeStamp
		return "true"
					

					
def readInfo():
		
	dataSaved="false" #keep on reading till you get the info
	actWeather = Weather()		

	while(dataSaved=="false"):
		# Get sensor data
		btemp = actWeather.getBTempData()
		hum  = actWeather.getHumData()
		temp =  actWeather.getTempData()
		pressure = actWeather.getPressData()
		altitude = actWeather.getAltData()
		moist = actWeather.getMoistData()
		currentDate = datetime.datetime.now().date()
		timeStamp =  datetime.datetime.now() 
		forecast = actWeather.checkPress()
		trend = actWeather.getTrend()
		dewPoint = actWeather.getDewPoint()
		spezF = actWeather.getspezF()	
		sattF = actWeather.getsattF()
		print "Vorhersage           = %.20s " % forecast
		print "Trend                = %.1s " % trend
		print "Temperatur           = %.2f C" % temp
		print "rel Feuchte          = %.2f " % hum
		print "Boden Feuchte        = %.2f " % moist 
		print "Barometer Temperatur = %.2f C" % btemp
		print "Luftdruck            = %.2f hPa" % pressure
		print "Hoehe                = %.2f m" % altitude	
		print "Taupunkt             = %.2f C" % dewPoint
		print "spez. Feuchte        = %.2f g/m^3" % spezF
		print "saett. Feuchte       = %.2f g/m^3" % sattF
		return saveToDatabase(forecast,trend,temp,hum,moist,btemp,pressure,altitude,dewPoint,spezF,sattF,currentDate,timeStamp)


status="false"
while(status!="true"):
	status=readInfo()

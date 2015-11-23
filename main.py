#!/usr/bin/python
################################################################################################
# Name: 		Klima Monitor
#
# Beschreibung:	Das Projekt Klima Monitor ist eine Wettervorhersage basierend auf dem GrovePi+ 
#               und dem RaspberryPi B+. Es werden mittels Sensoren Temperatur, Luftfeuchtigkeit und
#				Luftdruck gemessen und eine Vorhersage berechnet.
#				Das Projekt besteht aus zwei Teilen:
#				Teil 1 ist das WordPress Plugin Klima Monitor zur Darstellung der Werte und der
#				Wettervorhersage
#				Teil 2 die Erfassung der Werte und deren Verarbeitung
# Version: 		1.5.0
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
# 1.1.1 -	Change of package structure
# 1.2.0 -	Einbindung der Wettervorhersage
# 1.2.1 -	Auslagerung der Sensordatenermittlung in eigene Klasse
# 1.2.2 -	Speicherung der Wetterdaten im JSON-Format
# 1.2.3 - 	Fehler in der Luftdruckermittlung, Werte ueber 1200
# 1.3.0 - 	Trendberechnung duch Trendfunktion ersetzt, WICHTIG: forecast.json manuell loeschen
# 1.3.1 -	Fehler in der Trendberechnung, nach einer Sturmwarnung, WICHTIG: forecast.json manuell loeschen
# 1.4.0 -   Uebermittlung der Sensordaten an Telegram Bot
# 1.4.1 -   Uebermittlung der Sensordaten an Telegram Bot mit Vorhersage und Icon
# 1.5.0 -   Eigenes Program zur Kommunikation mit Telegram
################################################################################################

import subprocess 
import re 
import os 
import sys 
import time 
import MySQLdb as mdb
import datetime
from classes.weather import Weather
from classes.sensor import Sensor

databaseUsername="USER"
databasePassword="PASSWORD" 
databaseName="DATABASENAME" 
databaseTable="DATABASETABLE"

path = os.path.dirname(os.path.abspath(sys.argv[0]))
backupFileLocation= path + "/files/dataBackup.txt"

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
	weatherInst = Weather()
	sensorInst = Sensor()
	while(dataSaved=="false"):
		# Get sensor data
		btemp = sensorInst.getBTempData()
		hum  = sensorInst.getHumData()
		temp =  sensorInst.getTempData()
		pressure = sensorInst.getPressData()
		altitude = sensorInst.getAltData()
		moist = sensorInst.getMoistData()
		currentDate = datetime.datetime.now().date()
		timeStamp =  datetime.datetime.now() 
		forecast,trend = weatherInst.checkForecast()
		dewPoint = weatherInst.getDewPoint()
		spezF = weatherInst.getspezF()	
		sattF = weatherInst.getsattF()
        return saveToDatabase(forecast,trend,temp,hum,moist,btemp,pressure,altitude,dewPoint,spezF,sattF,currentDate,timeStamp)


status="false"
while(status!="true"):
	status=readInfo()

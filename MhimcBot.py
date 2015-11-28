#!/usr/bin/python
################################################################################################
# Name: 		My Home is my Castle BOT
#
# Beschreibung:	Kommuniziert mit Telegram Bot, die Chat_ID und der Token muss eingetragen werden
#               
# Version: 		1.0.0
# Author: 		Stefan Mayer
# Author URI: 	http://www.2komma5.org
# License: 		GPL2
# License URI: 	http://www.gnu.org/licenses/gpl-2.0.html
################################################################################################
# Changelog 
# 1.0.0 - 	Initial release
# 1.1.0 -   Camera Pi
################################################################################################
import logging
import subprocess 
import telegram
import json
import time
import datetime as dt
import picamera
from classes.weather import Weather
from classes.sensor import Sensor

token = 'TOKEN'
picture = 'Wetter.jpg'
bot = telegram.Bot(token)
camera = picamera.PiCamera()
camera.vflip = True
camera.hflip = True

def getForecastText(forecast):
	if forecast == 6:
		 text = "sonnig"
	elif forecast == 5:
		text = "heiter"
	elif forecast == 4:
		text = "bewoelkt"
	elif forecast == 3:
		text = "bedeckt"
	elif forecast == 2:
		text = "wechselhaft"
	elif forecast == 1:
		text = "vereinzelt Regen"
	elif forecast == 0:
		text = "Regen"
	elif forecast == -1:
		text = "Gewitter"
	else:
		text ="else"
	return text
	
def getForecastIcon(forecast):
	if forecast == 6:
		 icon = telegram.Emoji.SUN_WITH_FACE
	elif forecast == 5:
		icon = telegram.Emoji.SUN_BEHIND_CLOUD
	elif forecast == 4:
		icon = telegram.Emoji.SUN_BEHIND_CLOUD
	elif forecast == 3:
		icon = telegram.Emoji.CLOUD
	elif forecast == 2:
		icon = telegram.Emoji.CLOUD
	elif forecast == 1:
		icon = telegram.Emoji.UMBRELLA_WITH_RAIN_DROPS
	elif forecast == 0:
		icon = telegram.Emoji.UMBRELLA_WITH_RAIN_DROPS
	elif forecast == -1:
		icon = telegram.Emoji.HIGH_VOLTAGE_SIGN
	else:
		icon ="else"
	return icon	

def getPicture(chat_id):
	pic_time = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	camera.annotate_text = pic_time
	try:
		camera.capture(picture)
		time.sleep(4)
		photo = open('/home/pi/klimamonitor/Wetter.jpg', 'rb')
		bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
		bot.sendPhoto(chat_id=chat_id, photo=photo)
		photo.close()
		return pic_time
	except:
		return 'Cam Error'

	
	
def getWeather():
	weatherInst = Weather()
	sensorInst = Sensor()
	# Get sensor data
	hum  = sensorInst.getHumData()
	temp =  sensorInst.getTempData()
	pressure = sensorInst.getPressData()
	forecast,trend = weatherInst.checkForecast()

	text = "Vorhersage: " + getForecastText(forecast) + " " + getForecastIcon(forecast) + "\nTrend: " + trend + "\nLuftdruck = %.2f hPa" % pressure + "\nrel Feuchte = %.2f " % hum  + "\nTemperatur = %.2f C" % temp
	return text 

		
def check_chat_id(chat_id):
	ok_list = [CHATID]  
	if chat_id in ok_list:
		bol = True
	else:
		bol = False
	return bol
	
def main():
	logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

	
	try:
		LAST_UPDATE_ID = bot.getUpdates()[-1].update_id  # Get lastest update
		
		
		while True:
			for update in bot.getUpdates(offset=LAST_UPDATE_ID, timeout=10):
				text = update.message.text
				chat_id = update.message.chat.id
				print update.message
				error_msg = 'Achtung eine invalide Chat Id wurde verwendet'
				update_id = update.update_id
			
				if False == check_chat_id(chat_id):
					bot.sendMessage(chat_id=chat_id, text='Invalid Chat Id')
					bot.sendMessage(chat_id='18051286', text=error_msg)
					LAST_UPDATE_ID = update_id + 1
					break

				if text:
					bot.sendMessage(chat_id=chat_id, text=command(chat_id,text))
					LAST_UPDATE_ID = update_id + 1
	except:
		print 'noch nix in der Update Liste'
	

def command(chat_id,command_txt):
	bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
	if command_txt == '/wetter':
		msg = getWeather()		
	elif command_txt == '/pic':
		msg = getPicture(chat_id)	
	else:
		msg = 'Falscher Befehl'
	return msg

if __name__ == '__main__':
	status="False"
	while(status!="True"):
		status=main()
		time.sleep(5)

	


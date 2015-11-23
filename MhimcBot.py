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
################################################################################################
import logging
import subprocess 
import telegram
from classes.weather import Weather
from classes.sensor import Sensor

token = 'TOKEN'

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
    logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    bot = telegram.Bot(token)
    LAST_UPDATE_ID = bot.getUpdates()[-1].update_id  # Get lastest update

    while True:
        for update in bot.getUpdates(offset=LAST_UPDATE_ID, timeout=10):
			text = update.message.text
			chat_id = update.message.chat.id
			#print chat_id
			update_id = update.update_id
			
			if False == check_chat_id(chat_id):
				bot.sendMessage(chat_id=chat_id, text='Invalid Chat Id')
				LAST_UPDATE_ID = update_id + 1
				break

			if text:
				bot.sendMessage(chat_id=chat_id, text=command(text))
				LAST_UPDATE_ID = update_id + 1


def command(command_txt):
	if command_txt == '/wetter':
		msg = getWeather()
	else:
		msg = 'Wrong command'
	return msg

if __name__ == '__main__':
    main()

#!/usr/bin/python
################################################################################################
# Name: 		TeleBot
#
# Beschreibung:	Kommuniziert mit Telegram Bot
# Author: 		Stefan Mayer
# Author URI: 	http://www.2komma5.org
# License: 		GPL2
# License URI: 	http://www.gnu.org/licenses/gpl-2.0.html
################################################################################################
import subprocess 
import telegram

class TeleBot():
	def getForecastText(self,forecast):
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
		
	def getForecastIcon(self,forecast):
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
		
	def talkToTeleBot(self,token,forecast,trend,temp,hum,moist,btemp,pressure,altitude,dewPoint,spezF,sattF,currentDate,timeStamp):
		bot = telegram.Bot(token)
		print bot.getMe()
		#chat_id = bot.getUpdates()[-1].message.chat_id
		chat_id = 'chat_id'
		#print chat_id
		text = "Vorhersage: " + self.getForecastText(forecast) + " " + self.getForecastIcon(forecast) + "\nTrend: " + trend + "\nLuftdruck = %.2f hPa" % pressure + "\nrel Feuchte = %.2f " % hum  + "\nTemperatur = %.2f C" % temp
		bot.sendMessage(chat_id, text)

		return "Message transfer ok" 
	
	
	

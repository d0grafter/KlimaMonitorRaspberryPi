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
	
	def talkToTeleBot(self,token,forecast,trend,temp,hum,moist,btemp,pressure,altitude,dewPoint,spezF,sattF,currentDate,timeStamp):
		bot = telegram.Bot(token)
		print bot.getMe()
		#chat_id = bot.getUpdates()[-1].message.chat_id
		chat_id = 'chat_id'
		#print chat_id
		text = "Luftdruck = %.2f hPa" % pressure + " rel Feuchte = %.2f " % hum  + " Temperatur = %.2f C" % temp
		bot.sendMessage(chat_id, text)

		return "Message transfer ok" 
			
	

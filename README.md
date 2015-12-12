# Name: 		Klima Monitor
## Beschreibung:	
Das Projekt Klima Monitor ist eine Wettervorhersage basierend auf dem GrovePi+ 
und dem RaspberryPi B+. Es werden mittels Sensoren Temperatur, Luftfeuchtigkeit und
Luftdruck gemessen und eine Vorhersage berechnet.

Das Projekt besteht aus zwei Teilen:

	Teil 1 ist das WordPress Plugin Klima Monitor zur Darstellung der Werte und der Wettervorhersage
	Teil 2 die Erfassung der Werte und deren Verarbeitung
Version: 	1.4.0

Author: 	Stefan Mayer

Author URI:	http://www.2komma5.org

License: 	GPL2

License URI: 	http://www.gnu.org/licenses/gpl-2.0.html

## Changelog 

1.0.0 - Initial release

1.1.0 - Speicherung der Sensordatenin lokale Datei, falls keine Datenbankverbindung besteht
      	Nach erneutem Aufbau der Verbindung, werden die Daten aus der lokalen Datei 
	automatisch in die Datenbank uebernommen

1.1.1 -	Change of package structure

1.2.0 -	Einbindung der Wettervorhersage

1.2.1 -	Auslagerung der Sensordatenermittlung in eigene Klasse

1.2.2 -	Speicherung der Wetterdaten im JSON-Format

1.2.3 -	Fehler in der Luftdruckermittlung, Werte ueber 1200

1.3.0 -	Trendberechnung duch Trendfunktion ersetzt, WICHTIG: forecast.json manuell loeschen

1.3.1 -	Fehler in der Trendberechnung, nach einer Sturmwarnung, WICHTIG: forecast.json manuell loeschen

1.4.0 - Uebermittlung der Sensordaten an Telegram Bot in eigenem Programm MhimcBot.py
################################################################################################


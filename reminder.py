#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
SMS Reminder version 1.0

Copyright (C)2008 Petr Nohejl, jestrab.net

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

This program comes with ABSOLUTELY NO WARRANTY!
"""

### IMPORT #####################################################################

import smtplib
import string
import time



### CONFIG #####################################################################

FROMADDR = "stud.fit.vutbr.cz"		# server
LOGIN = "xlogin00"					# login na mail
PASSWD = "pass"						# heslo na mail
TOADDR  = "nick@vodafonemail.cz"	# mobilni email
HEADER = "From: %s@%s\r\nTo: %s\r\n\r\n" % (LOGIN, FROMADDR, TOADDR)
SMTP = "eva.fit.vutbr.cz"			# smtp server

FILE = "reminder"					# konfiguracni soubor s daty
REFRESH = 300 						# refresh time v sekundach



### SEND MAIL ##################################################################

# funkce odesle email / sms
def SendMail(msg):
    server = smtplib.SMTP(SMTP, 587)
    #server.starttls()
    server.login(LOGIN, PASSWD)
    server.sendmail(FROMADDR, TOADDR, HEADER + str(msg))
    server.quit()



### LOAD DATA ##################################################################

# funkce nacte data ze souboru
def LoadData():
	file = open(FILE,"r")	# otevre soubor pro cteni
	data = []
	
	while(1):
		line = file.readline()	# nacte radek
		
		# konec souboru
		if(line == ""):
			break
			
		line = string.split(line,"#",1)[0]	# odstraneni komentaru
		pieces = string.rsplit(line,"::",1)	# rozdeleni na 2 casti - casove udaje a text
		
		if((string.count(line, "::") != 4) or (len(pieces) != 2)):
			continue	# chybny format dat
		else:
			# odstraneni bilych znaku
			pieces[0] = string.strip(pieces[0])
			pieces[0] = string.replace(pieces[0], " ", "")
			pieces[0] = string.replace(pieces[0], "\t", "")
			pieces[1] = string.strip(pieces[1])
			
			piecesTime = string.split(pieces[0], "::")
			
			# osetreni chyb
			if(pieces[1] == "" or len(piecesTime) != 4):
				continue
				
			try:
				int(piecesTime[0])
				int(piecesTime[1])
				int(piecesTime[2])
				int(piecesTime[3])
			except:
				continue
			
			data.append(pieces)	# pripoji seznam k vyslednemu seznamu

	file.close	# uzavre soubor
	return data



### REMINDER ###################################################################

# funkce zpracovava data
def Reminder():
	while(1):
		data = LoadData()	# nacteni dat ze souboru
		#print data
		
		currentTime = time.localtime()				# aktualni cas ulozeny v n-tici
		currentStamp = time.mktime(currentTime)		# casova znamka
		#print currentStamp, currentTime
		
		for x in range(len(data)):
			pieces = string.split(data[x][0], "::")
			
			# cas udalosti ulozeny v n-tici
			dataTime = (time.localtime()[0], int(pieces[1]), int(pieces[0]), int(pieces[2]), int(pieces[3]), 0, -1, -1, -1)
			dataStamp = time.mktime(dataTime)	# casova znamka udalosti
			
			diff = dataStamp-currentStamp	# rozdil casu
			
			# bude se odesilat sms
			if(diff < REFRESH and diff >= 0):
				
				# ziskani casovych udaju
				currentDay = str(time.localtime()[2])
				currentMonth = str(time.localtime()[1])
				currentYear = str(time.localtime()[0])
				currentHour = str(time.localtime()[3])
				currentMinute = str(time.localtime()[4])
				currentSecond = str(time.localtime()[5])
				
				# osetreni casovych udaju
				if(len(currentDay) == 1): currentDay = "0" + currentDay
				if(len(currentMonth) == 1): currentMonth = "0" + currentMonth
				if(len(currentHour) == 1): currentHour = "0" + currentHour
				if(len(currentMinute) == 1): currentMinute = "0" + currentMinute
				if(len(currentSecond) == 1): currentSecond = "0" + currentSecond
				
				# kontrolni vypis
				print currentDay + "." + currentMonth + "." + currentYear + " " + currentHour + ":" + currentMinute + ":" + currentSecond + "   HEAD: " + data[x][0] + "   MESSAGE: " + data[x][1]
				
				# odeslani sms
				SendMail("REMINDER: " + data[x][1])
			
			#print dataStamp, dataTime, diff
		
		# uspani cyklu while
		time.sleep(REFRESH)



### MAIN #######################################################################

if (__name__=="__main__"):
	Reminder()
	

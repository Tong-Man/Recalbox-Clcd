#!/usr/bin/python
# coding=utf-8
"""
recalbox_clcd.py
Author       : Choum, original first script version from Godhunter74 with a lot of of inspiration and work from zzeromin, member of Raspberrypi Village
Creation Date: 08/15/2017
Blog         : https://forum.recalbox.com/topic/5777/relier-%C3%A0-un-%C3%A9cran-et-afficher-du-texte and original work : http://rasplay.org, http://forums.rasplay.org/, https://zzeromin.tumblr.com/
Thanks to    : Godhunter74, zzeromin smyani, zerocool, GreatKStar

Free and open for all to use. But put credit where credit is due.

#Reference:
I2C_LCD_driver developed by: Denis Pleic ( https://gist.github.com/DenisFromHR/cc863375a6e19dce359d )
IP_Script Developed by: AndyPi ( http://andypi.co.uk/ )
lcdScroll Developed by: Eric Pavey ( https://bitbucket.org/AK_Eric/my-pi-projects/src/28302f8f5657599e29cb5d55573d192b9fa30265/Adafruit_CharLCDPlate/lcdScroll.py?at=master&fileviewer=file-view-default )

#Notice:
recalbox_clcd.py require I2C_LCD_driver.py, lcdScroll.py

Small script written in Python for recalbox project (https://www.recalbox.com/) 
running on Raspberry Pi 1,2,3, which displays all neccessary info on a 16x2 LCD display
#Features:
1. Current date and time, IP address of eth0, wlan0
2. CPU temperature and speed
3. Emulation and ROM information extracet from gamelist                      !!!!!!!!!!     YOU MUST SCRAPP YOUR ROMS        !!!!!!!!!!!!!
"""

import I2C_LCD_driver
import os
from os import popen
from sys import exit
from subprocess import *
from time import *
from datetime import datetime
from lcdScroll import Scroller
import string
import locale
import unicodedata

# For DE language -> locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')

def run_cmd(cmd):
   # runs whatever is in the cmd variable in the terminal
   p = Popen(cmd, shell=True, stdout=PIPE)
   output = p.communicate()[0]
   return output

def get_cpu_temp():
   # get the cpu temp
   tempFile = open("/sys/class/thermal/thermal_zone0/temp")
   cpu_temp = tempFile.read()
   tempFile.close()
   return float(cpu_temp)/1000

def get_cpu_speed():
   # get the cpu speed
   tempFile = open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq")
   cpu_speed = tempFile.read()
   tempFile.close()
   return float(cpu_speed)/1000

def getTextInside (fullText, textBefore, textAfter, index) :
	begin = -1
	end = -1
	if index < len(fullText[index:]) - len(textBefore):
		begin = fullText[index:].find(textBefore) 	#on cherche le debut 
		if len(fullText[index:]) >= begin +len(textBefore)+len(textAfter):
			end = fullText[index+begin +len(textBefore):].find(textAfter)		#on cherche la fin 
	if begin ==-1 or end ==-1 : #-1 = pas trouve, trouve est forcement entre 0 et len(fullText)-1
		return (index, "pas_trouve")		# si on a pas retrouve le debut ou la fin on retourne une chaine vide 
	else:
		return (index + begin+  end + len(textAfter), fullText[index + begin+ len(textBefore): index + begin+ len(textBefore)+ end])	# sinon on retourne ce qui se trouve entre les 2

mylcd = I2C_LCD_driver.lcd()
mylcd.lcd_clear()

#get ip address of eth0 connection
cmdeth = "ip addr show eth0 | grep 'inet ' | awk '{print $2}' | cut -d/ -f1"
#get ip address of wlan0 connection
cmd = "ip addr show wlan0 | grep 'inet ' | awk '{print $2}' | cut -d/ -f1"
#cmd = "ip addr show wlan1 | grep 'inet ' | awk '{print $2}' | cut -d/ -f1"

old_Temp = new_Temp = get_cpu_temp()
old_Speed = new_Speed = get_cpu_speed()
#draw icons not existing in [a-z]
icons = [
                [ 0b00000, 0b11111, 0b11011, 0b10001, 0b10001, 0b10001, 0b11111, 0b00000 ], # Ethernet icon
                [ 0b00000, 0b00000, 0b00001, 0b00001, 0b00101, 0b00101, 0b10101, 0b00000 ], # Wireless icon
                [ 0b00000, 0b10001, 0b01010, 0b00100, 0b01010, 0b10001, 0b00000, 0b00000 ], # recalbox logo Cross
                [ 0b00000, 0b00100, 0b01110, 0b01010, 0b10001, 0b11111, 0b00000, 0b00000 ], # recalbox logo Triangle
                [ 0b00000, 0b01110, 0b10001, 0b10001, 0b10001, 0b01110, 0b00000, 0b00000 ], # recalbox logo Circle.
                [ 0b00000, 0b11111, 0b10001, 0b10001, 0b10001, 0b11111, 0b00000, 0b00000 ]  # recalbox logo Square
        ]

# Load logo chars (icons)
mylcd.lcd_load_custom_chars(icons)

#display first message on screen
mylcd.lcd_display_string("PI STATION 3", 1, 2) #firstline
mylcd.lcd_display_string(" "+unichr(2)+" "+unichr(3)+" "+unichr(4)+" "+unichr(5), 2, 3) #secondline
sleep(5) # 5 sec delay
mylcd.lcd_clear()
# display a second message on screen
mylcd.lcd_display_string("www.recalbox.com", 1) #firstline
mylcd.lcd_display_string("RECALBOX v4.1", 2, 1) #secondline
sleep(5) # 5 sec delay
mylcd.lcd_clear() #delete strings on screen

while 1:
   
   mylcd.lcd_clear()
   sec = 0
   while ( sec < 5 ) :
      # wlan ip address
      ipaddr = run_cmd(cmd).replace("\n","")

      # selection of wlan or eth address
      length = len(ipaddr)
      space = ""

      if length == 0 :
         ipaddr = run_cmd(cmdeth).replace("\n","")

         if len(ipaddr) == 0 :
            ipaddr = unichr(0)+unichr(1)+" Hors Ligne"
         else:
            if len(ipaddr) == 15 :
               ipaddr = unichr(0)+run_cmd(cmdeth)
            else :
               for i in range( 15-len(ipaddr) ) :
                  space = space + " "
               ipaddr = unichr(0)+space+run_cmd(cmdeth)
	
      else :
         if len(ipaddr) == 15 :
            ipaddr = unichr(1)+run_cmd(cmd)
         else :
            for i in range( 15-len(ipaddr) ) :
                space = space + " "
            ipaddr = unichr(1)+space+run_cmd(cmd)

      #print datetime.now().strftime( "%b %d  %H:%M:%S" )
      #print "IP " + str( ipaddr )
	  #display the third message
	  # Fix for LCD that do not have European characters roms (ex HD77480A00)
	  # uncomment line below and comment the 2 next lines if you have an HD77480A02 which support European characters)
	  # mylcd.lcd_display_string( datetime.now().strftime( "%b %d %H:%M:%S" ), 1, 0 )
      datefix = datetime.now().strftime('%d %b %H:%M:%S').decode('utf-8')
      datefix = unicodedata.normalize('NFKD', datefix).encode('ASCII', 'ignore')
      mylcd.lcd_display_string( datefix , 1, 0 )
      mylcd.lcd_display_string( ipaddr, 2, 0 )
      sec = sec + 1
      sleep(1)

   mylcd.lcd_clear()
   sec = 0
   while ( sec < 5 ) :
      space = ""
      # cpu Temp & Speed information
      new_Temp = get_cpu_temp()
      new_Speed = int( get_cpu_speed() )

      if old_Temp != new_Temp or old_Speed != new_Speed :
         old_Temp = new_Temp
         old_Speed = new_Speed
         #print "CPU Temp: " + str( new_Temp )
         #print "CPU Speed: " + str( new_Speed )
	 for i in range( 5 - len( str(new_Speed) ) ) :
             space = space + " "
         mylcd.lcd_display_string( "Temp CPU :" + str( new_Temp ), 1, 0 )
         mylcd.lcd_display_string( "Freq CPU : " + space + str( new_Speed ), 2, 0 )
         sec = sec + 1  
         sleep(1)

   mylcd.lcd_clear()
   sec = 0
   while ( sec < 1 ) :
      # show system & rom file information
         result = run_cmd("ps | grep emulatorlauncher.py | grep -v 'c python' | grep -v grep")
         if result != "" :
            (index, systeme) = getTextInside( result, "-system ", " -rom ",0)	
            #~ index = 0
            (index,rom ) = getTextInside( result, "-rom ", " -emulator ",0)
			# Ignorer si kodi car pas de gamelist.xml, ni de rom
            if systeme != "kodi" :
				#print "systeme [" + systeme + "]"
				#print "rom [" + rom + "]"
				# Cas particulier si sous dossier dans le scrap pour cavestory et la dreamcast.
				if systeme == "cavestory" :
					nom_gamelist = os.path.basename(rom)
					nom_gamelist = "./CaveStory/"+nom_gamelist
				elif systeme == "dreamcast" :
					nom_gamelist = rom[31:]
					nom_gamelist = "./"+nom_gamelist
				else :
					nom_gamelist= os.path.basename(rom)
					nom_gamelist = "./"+nom_gamelist
				# Remplace & Par valeur XML pour retrouver le jeu dans gamelist.xml
				nom_gamelist = string.replace(nom_gamelist,'&','&amp;')
				#print "nom_gamelist ["+nom_gamelist +"]"
				f=open("/recalbox/share/roms/"+ systeme + "/gamelist.xml", 'r') 	# on ouvre le fichier 
				# ici on considere que le fichier est dans le meme repertoire mais tu peux aller le chercher ou tu veux avec un chemin absolu ex= "/mondossier/gamelist.xml" ou relatif ex= "../mondossier/gamelist.xml"
				buf = f.read()				# on lit tout ce qu'il y a dedans (stocke dans un buffer en RAM)
				f.close()					#on ferme le fichier          
				(index,gameData) = getTextInside( buf, "<path>" + nom_gamelist, "</game>",0)
				#print gameData
				#initialize all the <balise> to extract from gamelist
				name = ""
				desc = ""
				image = ""
				rating = ""
				releasedate = ""
				developer = ""
				publisher = ""
				genre = ""
				players = ""

				if gameData != "pas_trouve": # test si jeu trouvé dans gamelist.xml 
					(index2,name) = getTextInside( gameData, "<name>","</name>",0)	# name 
					(index2,desc) = getTextInside( gameData, "<desc>","</desc>",0)	#desc
					(index2,image) = getTextInside( gameData, "<image>","</image>",0)	#image
					(index2,rating) =  getTextInside( gameData, "<rating>","</rating>",0)	#rating         
					(index2,releasedate) = getTextInside( gameData, "<releasedate>","</releasedate>",0)	# releasedate 
					(index2,developer) = getTextInside( gameData, "<developer>","</developer>",0)	#developer
					(index2,publisher) = getTextInside( gameData, "<publisher>","</publisher>",0)	#publisher
					(index2,genre) =  getTextInside( gameData, "<genre>","</genre>",0)	#genre         
					(index2,players) =  getTextInside( gameData, "<players>","</players>",0)	#players
					name = string.replace(name,'&amp;','&')	# Fix for & xml characters
					#print "name [" + name + "] description [" + desc + "] image [" + image + "] rating [" + str(rating) + "] releasedate [" + releasedate[:-11] + "] developer [" + developer + "] publisher [" + publisher + "] genre [" + genre + "] players [" + players + "]"
					systemMap = { 
					# Nintendo
					"snes":"Super Nes", # Super Famicon
					"nes":"Nes ", # Famicom
					"n64":"Nintendo 64",
					"gba":"GameBoy Advance",
					"gb":"GameBoy",
					"gbc":"GameBoy Color",
					"fds":"Famicom Disk System",
					"virtualboy":"Virtual Boy",
					"gamecube":"GameCube",
					"wii":"Wii",
					#Sega
					"sg1000":"Sega Game 1000",
					"mastersystem":"Master System", #Sega Mark III
					"megadrive":"Mega Drive", #Sega Genesis
					"gamegear":"Game Gear",
					"sega32x":"Mega Drive 32X ", #Genesis 32X
					"segacd":"Mega-CD", #Sega CD
					"dreamcast":"Dreamcast",
					# Arcade
					"neogeo":"Neo-Geo",
					"mame":"MAME-libretro",
					"fba":"FinalBurn Alpha",
					"fba_libretro":"FinalBurn Alpha libreretro",
					"advancemame":"Advance MAME",
					# Computers
					"msx":"MSX",
					"msx1":"MSX1",
					"msx2":"MSX2",
					"amiga":"Amiga",
					"amstradcpc":"Amstrad CPC",
					"apple2":"Apple II",
					"atarist":"Atari ST",
					"zxspectrum":"ZX Spectrum",
					"o2em":"Odyssey 2",
					"zx81":"Sinclair ZX81",
					"dos":"MS-DOS",
					"c64":"Commodore 64",
					# autres
					"ngp":"Neo-Geo Pocket",
					"ngpc":"Neo-Geo Pocket Color",
					"gw":"Game and Watch",
					"vectrex":"Vectrex",
					"lynx":"Atari Lynx",
					"lutro":"Lutro",
					"wswan":"WonderSwan",
					"wswanc":"WonderSwan Color",
					"pcengine":"PC-Engine", #TurboGrafx-16 
					"pcenginecd":"PC-Engine CD", #TurboGrafx-CD
					"supergrafx":"PC Engine SuperGrafx",
					"atari2600":"Atari 2600",
					"atari7800":"Atari 7800",
					"prboom":"PrBoom",
					"cavestory":"Cave Story",
					"scummvm":"ScummVM",
					"colecovision":"ColecoVision",
					"psx":"PlayStation",
					"psp":"PSPortable",    # PlayStation Portable
					# Logiciels
					"kodi":"KODI",
					"imageviewer":"Visionneuse d'images",		
					"ports":"Ports",
					"notice":"TURN OFF",
					}
					system = name[:16]
					plateforme = systemMap.get(systeme) 			
					rom = "Titre : " + name + " - Plateforme : " + plateforme + " - Genre : " + genre + " - Joueur(s) : " + players + " - Note : " + str(rating) + " - Date de sortie : " + releasedate[:-11] + " par " + developer + " pour " + publisher + "."
					#print "firstline : [" + firstline + "]"
					#print "secondline : [" + secondline + "]"
					# Comment 4 next lines if you have an HD77480A02 which support European characters
					system = system.decode('utf-8')
					system = unicodedata.normalize('NFKD', system).encode('ASCII', 'ignore')
					rom = rom.decode('utf-8')
					rom = unicodedata.normalize('NFKD', rom).encode('ASCII', 'ignore')
					flag = "TURN OFF"
					lines = rom
					wait = 0
					speed = 0.1

					# Create scroller instance:
					scroller = Scroller(lines=lines)
					while True :
						mylcd.lcd_clear()
						if wait < 11 and systeme != flag:
							message = scroller.scroll()       
							mylcd.lcd_display_string( "%s" %(system), 1, 0 )
							mylcd.lcd_display_string( "%s" %(message), 2 )
							sleep(speed)
							wait = wait + 0.1
						else :
							break
				sec = sec + 1
				sleep(1)
            else :
				# A dev affichage pour kodi
				sec = sec + 1
         else :
				sec=sec + 1
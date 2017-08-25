#!/usr/bin/python
# coding=utf-8
"""
recalbox_clcd_off.py
Author       : Choum
Creation Date: 08/16/2017

Free and open for all to use. But put credit where credit is due.

#Reference:
I2C_LCD_driver developed by: Denis Pleic https://gist.github.com/DenisFromHR/cc863375a6e19dce359d
lcdScroll Developed by: Eric Pavey
    https://bitbucket.org/AK_Eric/my-pi-projects/src/28302f8f5657/Adafruit_CharLCDPlate/?at=master

#Notice:
recalbox_clcd_off.py require I2C_LCD_driver.py

Small script written in Python for recalbox project (https://www.recalbox.com/)
running on Raspberry Pi 1,2,3
#Features:
Display a message when a shutdown (STOP) is launch by the daemon S97LCDInfoText
after killing recalbox_clcd.py process then cut LCD backlight

If you have a model HD44780A02 (support ASCII + european fonts), and want to display accented
characters, you will have to comment and uncomment some line in the script.
Search 'HD44780A02' comment in the script.
"""

from time import sleep
import unicodedata # useless if HD44780A02, comment or delete
import I2C_LCD_driver

def get_language():
    """ find the language in recalbox.conf file and use translate texts"""
    fic = open("/recalbox/share/system/recalbox.conf", 'r')
    for line in fic:
        if 'system.language=' in line:
            lang = line.replace("system.language=", "")
            lang = lang.replace("\n", "")
            break
    else:
        lang = "en_US"
    fic.close()
    print lang
    # All Texts to translate are below, missing turkisk, chinese, basque.
    if lang == "fr_FR":
        txt = "Extinction"
    elif lang == "de_DE":
        txt = "Stoppen"
    elif lang == "pt_BR":
        txt = "Extinção"
    elif lang == "es_ES" or lang == "eu_ES":
        txt = "Extinción"
    elif lang == "it_IT":
        txt = "Estinzione"
    else:
        txt = "Shutdown"
    return txt

# useless if HD44780A02, comment or delete
def conv_ascii(entree):
    """ convert UTF-8 string to ASCII"""
    entree = entree.decode('utf-8')
    entree = unicodedata.normalize('NFKD', entree).encode('ASCII', 'ignore')
    return entree

TXT = get_language()
#remove next line if you have an HD44780A02
TXT = conv_ascii(TXT)
MYLCD = I2C_LCD_driver.lcd()
MYLCD.lcd_clear()
MYLCD.lcd_display_string("PI STATION 3", 1, 2)
MYLCD.lcd_display_string(TXT, 2, 3) # Display a shutdown message when recalbox is turn off.
sleep(2)
MYLCD.lcd_clear()
MYLCD.backlight(0) #Disable backlight

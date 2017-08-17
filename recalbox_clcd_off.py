#!/usr/bin/python
"""
recalbox_clcd_off.py
Author       : Choum
Creation Date: 08/16/2017
Thanks to    : zzeromin smyani, zerocool, GreatKStar

Free and open for all to use. But put credit where credit is due.

#Reference:
I2C_LCD_driver developed by: Denis Pleic ( https://gist.github.com/DenisFromHR/cc863375a6e19dce359d )
lcdScroll Developed by: Eric Pavey ( https://bitbucket.org/AK_Eric/my-pi-projects/src/28302f8f5657599e29cb5d55573d192b9fa30265/Adafruit_CharLCDPlate/lcdScroll.py?at=master&fileviewer=file-view-default )

#Notice:
recalbox_clcd_off.py require I2C_LCD_driver.py, lcdScroll.py

Small script written in Python for recalbox project (https://www.recalbox.com/) 
running on Raspberry Pi 1,2,3, use for shutdown message.
#Features:
Display a message when a shutdown is launch by the daemon S97LCDInfoText after killing recalbox_clcd.py process
"""

import I2C_LCD_driver
from lcdScroll import Scroller
from time import *
import string

mylcd = I2C_LCD_driver.lcd()
mylcd.lcd_clear()

#display first message on screen
mylcd.lcd_display_string("PI STATION 3", 1, 1) #firstline
mylcd.lcd_display_string("Extinction...", 2, 2) #secondline
sleep(2) # 3 sec delay
mylcd.lcd_clear()
mylcd.backlight(0)

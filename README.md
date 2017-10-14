## Recalbox-Clcd
Scrolling informations for Recalbox v4.x using 16x2 CLCD on raspberry pi 3

<img src="http://i.imgur.com/CGAyTAlm.jpg">

## About
Small script written in Python for Recalbox project ( http://recalbox.com/ ) 
running on Raspberry Pi 2,3, which displays all necessary info on a 16x2 CLCD display
**You must scrap your rom to make this script work correctly when playing.**

## Credits
* Original version of the recalbox script from Godhunter74
* Original project for retropie from zzeromin (https://github.com/zzeromin/RetroPie-Clcd)
* Thanks to zzeromin smyani, zerocool, GreatKStar
* Recalbox team http://www.recalbox.com

## Features
* Current Date and Time
* IP address of eth0, wlan0
* CPU Temperature and Speed
* Emulation and ROM informations
* Daemon provide to manage start/stop of the script

## Development Environment
* Raspberry Pi 3
* Recalbox v4.1
* 16x2 I2C HD447800 LCD (A00)

## Installation

#### Prerequisites

You will need an CLCD I2c like the HD44780 with rom A00 (Ascii support + japanese characters) or A02 (Ascii + European Characters)

<img src="http://i.imgur.com/YrDDhwUm.jpg">


#### Raspberry Pi I2C GPIO Pinout

Connection of the I2c to a raspberry pi 3

<img src="http://i.imgur.com/NKswbgr.png">



#### Activate I2C inside recalbox

* connect in ssh to your recalbox and mount partition to rw mode 
```
mount -o remount, rw /
```

* Edit /etc/modules.conf
* Add at the end of the file
```
i2c-bcm2708
i2c-dev
```

* Edit the /boot/config.txt
* add following lines in it:
```
#Activate I2C
dtparam=i2c1=on
dtparam=i2c_arm=on
```

* Edit the /boot/cmdline.txt
add at **the end of line**
```
bcm2708.vc_i2c_override=1
```
*  reboot your recalbox


#### Check I2C address 
You should check your I2C address of 16x2 CLCD as this device can have different adress.
Those are two address each other normally => 0x27 or 0x3f.

Execute the following command (could take some time to complete)
```
i2cdetect -y 1
```
<pre><code>
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- 27 -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --</code></pre>

In our example the I2C adress is 0x27

#### Scripts installation

* connect in ssh to your recalbox and mount partition to rw mode 
```
mount -o remount, rw /
```

* Copy 
        recalbox_clcd.py 
        recalbox_clcd_off.py
        I2C_LCD_driver.py
        lcdScroll.py 
    to **/recalbox/scripts** folder with winscp for example

* Copy 
        S97LCDInfoText 
    to **/etc/init.d/**
    
* then give execute right on all file

```
Chmod +x /recalbox/scripts/recalbox_clcd_off.py
Chmod +x /recalbox/scripts/recalbox_clcd_off.py
Chmod +x /recalbox/scripts/I2C_LCD_driver.py
Chmod +x /recalbox/scripts/lcdScroll.py
Chmod +x /etc/init.d/S97LCDInfoText
```

* edit line #22 in I2C_LCD_driver.py in /recalbox/scripts with the correct I2C adress, you have recover before (in our example :0x27).

<pre><code>nano I2C_LCD_driver.py

# LCD Address
ADDRESS = 0x27 # or 0x3f
</code></pre>

* reboot your recalbox, the script will now launch automatically on start, and exit and turn off LCD backlight during shutdown of your recalbox

## Important note

To make this script work with Scummvm, they should be scrap but the path in the gamelist.xml should be a folder and not the scummvm "fake file".
```
<path>./FT/</path>
instead of 
<path>./FT/ft.scummvm</path>
```

## Screenshots

<img src="http://i.imgur.com/PEAyQm2m.jpg">
<img src="http://i.imgur.com/fsXfArEm.jpg">
<img src="http://i.imgur.com/qesmRu6m.jpg">

## Reference

* https://forum.recalbox.com/topic/8689/script-clcd-display-on-recalbox
* https://forum.recalbox.com/topic/5777/relier-%C3%A0-un-%C3%A9cran-et-afficher-du-texte/121
RPi LCDInfo
===========

About
-----
This LCDInfo script requires the Adafruit RGB 16x2 LCD + Keypad Kit for RaspberryPi.
You can get ti here: http://www.adafruit.com/products/1109

To see the first beta version in action you can watch this video: http://youtu.be/P4EyNdhyyM0

Getting your Raspberry Pi ready
-------------------------------
First make sure that /etc/modules (```sudo nano /etc/modules```) contains this two lines:
```
i2c-bcm2708
i2c-dev
```

If you just added it reboot the Raspberry Pi or do the following:
```
sudo modprobe i2c-bcm2708
sudo modprobe i2c-dev
```

Finally you need to install some dependencies:
```
sudo apt-get install python-smbus i2c-tools
```

Using RPiLCD Info
-----------------

Just run it:
```
python main.py
```

If it doesn't works try to change in ```main.py``` this line:
```
lcd = Adafruit_CharLCDPlate()
```
to
```
lcd = Adafruit_CharLCDPlate(busnum = 0)
```
for a Rev 1 Raspberry Pi, or to
```
lcd = Adafruit_CharLCDPlate(busnum = 1)
```
for a Rev 2 Raspberry Pi.

Buttons
-------

```
SELECT:  Switch ON/OFF the LCD (it continues refreshing the content).
         If you hold SELECT the LCD powers off and the script exits.
UP:      Previous widget.
DOWN:    Next widget.
LEFT:    Previous LCD color.
RIGHT:   Next LCD color.
```

License: GPL v3
---------------
Copyright 2014 - Sergio Conde < skgsergio [at] gmail [dot] com >

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

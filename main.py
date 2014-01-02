#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2014 - Sergio Conde < skgsergio [at] gmail [dot] com >
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import os, urllib2, socket, re, datetime
from time import sleep
from multiprocessing import Process
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate

# Global Vars & Utils
MainSleepTime = 0.2 # Seconds
SelectItersToExit = 10 # SelectItersToKill * MainSleepTime = Seconds needed pushing select to exit

def centerText(text):
  return ' '*((16 - len(text)) / 2) + text

# Resources Widget
def getCPUUsage():
  return ' '.join(str(int(i*100)) + "%" for i in os.getloadavg())

def getRAMUsage():
  total = -1
  free = -1

  with open('/proc/meminfo') as f:
    for line in f:
      if line.split(':')[0] == 'MemTotal':
        total = int(line.split(':')[1].split()[0].strip()) / 1024
      elif line.split(':')[0] == 'MemFree':
        free = int(line.split(':')[1].split()[0].strip()) / 1024

      if total != -1 and free != -1: break

  return str(total-free) + "MB / " + str(total) + "MB"

def resourceMode(lcd):
  while True:
    lcd.clear()
    lcd.message(centerText(getCPUUsage()) + "\n" + centerText(getRAMUsage()))
    sleep(5)

# Internet Widget
def getExternalIP():
  try:
    req = urllib2.urlopen("http://checkip.dyndns.org/", timeout=0.5).read()
    exIP = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3}", req)[0]
    del req
  except:
    exIP = "Unknown Ext. IP"
  finally:
    return exIP

def getInternalIP():
  try:
    sok = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sok.connect(("google.com", 9))
    inIP = sok.getsockname()[0]
    del sok
  except:
    inIP = "Unknown Int. IP"
  finally:
    return inIP

def internetMode(lcd):
  while True:
    lcd.clear()
    lcd.message(centerText(getInternalIP()) + "\n" + centerText(getExternalIP()))
    sleep(10)

# Clock Widget
def clockMode(lcd):
  while True:
    lcd.clear()
    lcd.message(datetime.datetime.now().strftime("    %H:%M:%S\n   %d/%m/%Y"))
    sleep(1)

# Main
def main():
  # Init LCD
  lcd = Adafruit_CharLCDPlate()
  lcd.clear()

  # Color list
  col = (lcd.RED, lcd.YELLOW, lcd.GREEN, lcd.TEAL, lcd.BLUE, lcd.VIOLET)
  col_len = len(col)
  col_cur = 0

  # Status list
  st = (lcd.ON, lcd.OFF)
  st_len = len(st)
  st_cur = 0

  # Widget List
  widget = (clockMode, internetMode, resourceMode)
  widget_len = len(widget)
  widget_cur = 0

  # Power on the LCD and set the first color
  lcd.backlight(st[st_cur])
  lcd.backlight(col[col_cur])

  # Start the first widget
  p = Process(target=widget[widget_cur], args=(lcd,))
  p.start()

  longSelect = 0
  lastBtn = 0
  while True:
    # Read the buttons state.
    btns = lcd.buttons()

    if btns != 0:
      # Save the button state
      lastBtn = btns

      # SELECT Long Push: Kill script
      if btns == 1:
        longSelect += 1
        if longSelect >= SelectItersToExit:
          p.terminate()
          lcd.clear()
          lcd.backlight(lcd.OFF)
          lcd.stop()
          exit(0)

    elif btns == 0 and lastBtn != 0:
      # If this button event processing sends a command at the same time that the Widget does
      # it can produce unexcepted results so we stop the widget and restart it later.
      p.terminate()
      del p

      # SELECT: Backlight ON/OFF
      if lastBtn == 1:
        longSelect = 0
        st_cur = (st_cur + 1) % st_len
        if st[st_cur] == lcd.ON:
          lcd.backlight(col[col_cur])
        else:
          lcd.backlight(st[st_cur])

      # UP: Previous Widget
      elif lastBtn == 8:
        widget_cur = (widget_cur - 1) % widget_len

      # DOWN: Next Widget
      elif lastBtn == 4:
        widget_cur = (widget_cur + 1) % widget_len

      # LEFT: Prevous backlight color
      elif lastBtn == 16:
        col_cur = (col_cur - 1) % col_len
        lcd.backlight(col[col_cur])

      # RIGHT: Next backlight color
      elif lastBtn == 2:
        col_cur = (col_cur + 1) % col_len
        lcd.backlight(col[col_cur])

      # Reset the last button state
      lastBtn = 0
      # Restart the widget
      p = Process(target=widget[widget_cur], args=(lcd,))
      p.start()

    sleep(MainSleepTime)

if __name__ == "__main__":
  main()
